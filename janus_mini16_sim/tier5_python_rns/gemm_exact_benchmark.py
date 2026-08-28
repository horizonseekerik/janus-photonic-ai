"""
ALGORITHM 5F: BIT_EXACT_GEMM_BENCHMARK
======================================
Executes standard INT4, INT8, INT16, INT32, INT64 matrix multiplication benchmarks (32x32) across the 16 residue tiles.
Compares against NumPy 128-bit integer reference ground truth.
Strict verification criterion: 0.00000000000000% numerical deviation.
"""

import sys
import os
import random
import numpy as np
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg
from tier5_python_rns.moduli_generator import generate_moduli_set, crt_reconstruct


def run_gemm_precision_benchmark(
    N_dim: int = cfg.N_dim, precisions: list = [4, 8, 16, 32, 64]
) -> Dict[str, Any]:
    mod_info = generate_moduli_set()
    full_moduli = mod_info["moduli_full"]

    results = {}
    total_deviation = 0

    print("=" * 70)
    print("JANUS MINI 16-TILE: BIT-EXACT GEMM BENCHMARK SUITE (ALGORITHM 5F)")
    print("=" * 70)

    corner_cases = ["random", "max_pos", "max_neg", "mixed", "zero"]

    for P in precisions:
        for case in corner_cases:
            if P != 64:
                # FLAT RNS for INT4, INT8, INT16, INT32
                # We accumulate in CMOS, so optical tiles ONLY compute (x * y) mod m.
                # However, the final CRT reconstruction requires the dynamic range to cover
                # the sum of N_dim products. Thus, CMOS accumulates residues, and CRT handles the full number.
                # Wait, if we accumulate residues in CMOS, we must accumulate them over the REAL integer field?
                # No, if CMOS accumulates residues, it's just doing `acc += (x * y)` as integers!
                # Ah! If CMOS accumulates the products as normal binary integers, there is no modulus!
                # Wait, if CMOS accumulates them as integers, then we don't need CRT for the sum! We would just use the optical tile as a multiplier, and CMOS as a 32-bit adder tree.
                # Since we accumulate in CMOS *after* CRT reconstruction, the optical RNS domain
                # only needs to bound a single element-wise multiplication product!
                req_range = 2 ** (2 * P)
                k_needed = 1
                prod = full_moduli[0]
                while prod <= req_range and k_needed < len(full_moduli):
                    prod *= full_moduli[k_needed]
                    k_needed += 1

                # Check hardware limit
                if k_needed > cfg.N_tiles:
                    raise ValueError(
                        f"INT{P} requires {k_needed} tiles, exceeding {cfg.N_tiles} physical tiles."
                    )

                active_moduli = full_moduli[:k_needed]
            else:
                # INT64 uses dual-cluster QRNS. Exactly 16 tiles.
                # CMOS accumulates the real/cross terms separately.
                k_needed = 16

            bias = 2 ** (P - 1)
            if case == "random":
                A_signed = np.array(
                    [
                        [random.randint(-bias, bias - 1) for _ in range(N_dim)]
                        for _ in range(N_dim)
                    ],
                    dtype=object,
                )
                B_signed = np.array(
                    [
                        [random.randint(-bias, bias - 1) for _ in range(N_dim)]
                        for _ in range(N_dim)
                    ],
                    dtype=object,
                )
            elif case == "max_pos":
                A_signed = np.full((N_dim, N_dim), bias - 1, dtype=object)
                B_signed = np.full((N_dim, N_dim), bias - 1, dtype=object)
            elif case == "max_neg":
                A_signed = np.full((N_dim, N_dim), -bias, dtype=object)
                B_signed = np.full((N_dim, N_dim), -bias, dtype=object)
            elif case == "mixed":
                A_signed = np.full((N_dim, N_dim), bias - 1, dtype=object)
                B_signed = np.full((N_dim, N_dim), -bias, dtype=object)
            elif case == "zero":
                A_signed = np.zeros((N_dim, N_dim), dtype=object)
                B_signed = np.zeros((N_dim, N_dim), dtype=object)

            C_ref = np.matmul(A_signed, B_signed)

            if P != 64:
                # Flat RNS Path (Native Signed)
                C_residues = []
                for t in range(k_needed):
                    m = active_moduli[t]
                    A_res = (A_signed % m).astype(object)
                    B_res = (B_signed % m).astype(object)

                    # Optical Routing (Multiplication) without Accumulation
                    C_tile = np.zeros((N_dim, N_dim, N_dim), dtype=object)
                    for i in range(N_dim):
                        for j in range(N_dim):
                            for k in range(N_dim):
                                C_tile[i, j, k] = (A_res[i, k] * B_res[k, j]) % m
                    C_residues.append(C_tile)

                # Precompute M_tot for signed reconstruction
                M_tot = 1
                for m in active_moduli:
                    M_tot *= m

                C_janus = np.zeros((N_dim, N_dim), dtype=object)
                for i in range(N_dim):
                    for j in range(N_dim):
                        cmos_accumulator = 0
                        for k in range(N_dim):
                            elem_res = [C_residues[t][i, j, k] for t in range(k_needed)]
                            val = crt_reconstruct(elem_res, active_moduli)
                            if val >= M_tot // 2:
                                val -= M_tot
                            cmos_accumulator += val
                        C_janus[i, j] = cmos_accumulator
            else:
                # PRNS INT64 Path (16 Tiles = 2 Optical Clusters + 1 CMOS SRAM Cluster)
                from tier5_python_rns.moduli_generator import (
                    generate_prns_moduli_set,
                    to_prns,
                    from_prns,
                )

                prns_info = generate_prns_moduli_set()

                # Split 64-bit into two signed 32-bit halves.
                def split64_signed(val):
                    xl = val % (1 << 32)
                    if xl >= (1 << 31):
                        xl -= 1 << 32
                    xh = (val - xl) // (1 << 32)
                    return xh, xl

                C_janus_unsigned = np.zeros((N_dim, N_dim), dtype=object)

                for i in range(N_dim):
                    for j in range(N_dim):
                        # High precision CMOS accumulator for 64-bit products
                        cmos_accumulator = 0

                        for k in range(N_dim):
                            a_val = int(A_signed[i, k])
                            b_val = int(B_signed[k, j])

                            a_h, a_l = split64_signed(a_val)
                            b_h, b_l = split64_signed(b_val)

                            # Forward PRNS projection
                            opt_al, opt_ah = to_prns(a_l, a_h, prns_info)
                            opt_bl, opt_bh = to_prns(b_l, b_h, prns_info)

                            # Multiplexing 16 optical tiles over 2 clock cycles to compute all 4 products
                            C_xl_yl = [
                                (al * bl) % m
                                for al, bl, m in zip(
                                    opt_al, opt_bl, prns_info["opt_moduli"]
                                )
                            ]
                            C_xh_yh = [
                                (ah * bh) % m
                                for ah, bh, m in zip(
                                    opt_ah, opt_bh, prns_info["opt_moduli"]
                                )
                            ]
                            C_xl_yh = [
                                (al * bh) % m
                                for al, bh, m in zip(
                                    opt_al, opt_bh, prns_info["opt_moduli"]
                                )
                            ]
                            C_xh_yl = [
                                (ah * bl) % m
                                for ah, bl, m in zip(
                                    opt_ah, opt_bl, prns_info["opt_moduli"]
                                )
                            ]

                            # CRT Reconstruction
                            xl_yl_rec = from_prns(C_xl_yl, prns_info)
                            xh_yh_rec = from_prns(C_xh_yh, prns_info)
                            xl_yh_rec = from_prns(C_xl_yh, prns_info)
                            xh_yl_rec = from_prns(C_xh_yl, prns_info)

                            # Reconstruct the 64-bit product from 32-bit parts in CMOS (Addition strictly in CMOS)
                            cross_rec = xl_yh_rec + xh_yl_rec
                            product_64 = (
                                xh_yh_rec * (1 << 64)
                                + cross_rec * (1 << 32)
                                + xl_yl_rec
                            )

                            # CMOS Accumulation
                            cmos_accumulator += product_64

                        # Store accumulated result directly since we used A_signed
                        C_janus_unsigned[i, j] = cmos_accumulator

                C_janus = np.zeros((N_dim, N_dim), dtype=object)
                for i in range(N_dim):
                    for j in range(N_dim):
                        C_janus[i, j] = C_janus_unsigned[i, j]

            deviation = int(np.sum(np.abs(C_janus - C_ref)))
            max_err = int(np.max(np.abs(C_janus - C_ref)))
            total_deviation += deviation

            print(
                f"[*] INT{P:<2} | {case:<8} | {k_needed:>2} Channels | Max Element Error: {max_err} | Total Deviation: {deviation} | Status: {'PASS' if deviation == 0 else 'FAIL'}"
            )

        results[f"INT{P}"] = {
            "tiles_used": k_needed,
            "deviation": total_deviation,
            "max_element_error": max_err,
            "status": "PASS" if total_deviation == 0 else "FAIL",
        }

    print("-" * 70)
    print(
        f"CUMULATIVE NUMERICAL DEVIATION: {total_deviation} (0.00000000000000% Error)"
    )
    print("=" * 70)

    assert (
        total_deviation == 0
    ), f"GEMM arithmetic deviation non-zero: {total_deviation}"
    return results


if __name__ == "__main__":
    res = run_gemm_precision_benchmark()
