"""
ALGORITHM 5C: SPATIAL_ONE_HOT_ROUTER
====================================
Simulates spatial 1-hot 256-channel tensor contractions across 16 optical tiles.
Models 15-stage Beneš cyclic permutation routing for finite field residue multiplication,
followed by photodetection and Chinese Remainder Theorem reconstruction.
"""

import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg
from tier5_python_rns.moduli_generator import generate_moduli_set, crt_reconstruct


class SpatialOneHotTile:
    """Emulates a single 32x32 optical multiplier fabric with 256 spatial waveguides."""

    def __init__(
        self, modulus: int, N_dim: int = cfg.N_dim, N_alphabet: int = cfg.N_alphabet
    ):
        self.modulus = modulus
        self.N_dim = N_dim
        self.N_alphabet = N_alphabet

    def multiply_accumulate(self, A_res: np.ndarray, B_res: np.ndarray) -> np.ndarray:
        """
        Simulates hybrid opto-electronic tensor multiplication:
        1. Optical stage: 15-stage Beneš cyclic permutation routing:
           output_slot = (input_slot * weight) mod m. (No optical accumulation)
        2. CMOS stage: Photodetection converts spatial slot to binary integer,
           followed by electrical accumulation and final modulo reduction.
        """
        C_products = np.zeros((self.N_dim, self.N_dim, self.N_dim), dtype=np.int64)
        for i in range(self.N_dim):
            for j in range(self.N_dim):
                for k in range(self.N_dim):
                    a_val = int(A_res[i, k])
                    b_val = int(B_res[k, j])

                    optical_waveguide_out = (a_val * b_val) % self.modulus
                    C_products[i, j, k] = optical_waveguide_out
        return C_products


class SpatialOneHotAccelerator:
    """Master 16-Tile Monolithic Planar MVP Accelerator."""

    def __init__(self):
        self.mod_info = generate_moduli_set()
        self.moduli = self.mod_info["moduli_compute"]
        self.tiles = [SpatialOneHotTile(m) for m in self.moduli]

    def matmul(self, A_matrix: np.ndarray, B_matrix: np.ndarray) -> np.ndarray:
        """
        Performs exact matrix multiplication:
        1. Decomposes inputs into 16 residue channels.
        2. Routes through 16 parallel optical tiles to compute un-accumulated products.
        3. Reconstructs each product via CRT.
        4. Accumulates natively in CMOS.
        """
        N_dim = A_matrix.shape[0]
        C_products = []

        for t in range(cfg.N_tiles):
            m = self.moduli[t]
            A_res = A_matrix % m
            B_res = B_matrix % m
            C_products.append(self.tiles[t].multiply_accumulate(A_res, B_res))

        C_out = np.zeros((N_dim, N_dim), dtype=object)
        for i in range(N_dim):
            for j in range(N_dim):
                cmos_acc = 0
                for k in range(N_dim):
                    elem_res = [C_products[t][i, j, k] for t in range(cfg.N_tiles)]
                    cmos_acc += crt_reconstruct(
                        elem_res,
                        self.moduli,
                        self.mod_info["M_i"],
                        self.mod_info["N_i"],
                    )
                C_out[i, j] = cmos_acc
        return C_out


if __name__ == "__main__":
    acc = SpatialOneHotAccelerator()
    A = np.random.randint(0, 100, size=(cfg.N_dim, cfg.N_dim))
    B = np.random.randint(0, 100, size=(cfg.N_dim, cfg.N_dim))

    C_opt = acc.matmul(A, B)
    C_ref = np.matmul(A.astype(object), B.astype(object))

    diff = np.sum(np.abs(C_opt - C_ref))
    print(
        f"Spatial One-Hot 32x32 Tensor Contraction Deviation: {diff} (PASS)"
        if diff == 0
        else f"FAILED: {diff}"
    )
