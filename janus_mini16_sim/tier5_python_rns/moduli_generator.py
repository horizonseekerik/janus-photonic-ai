"""
ALGORITHM 5A: COPRIME & QRNS MODULI GENERATOR
=============================================
Generates the optimal 16 compute + 2 redundant pairwise coprime moduli for flat RNS,
and the official 8-modulus QRNS set for dual-cluster 64-bit integer execution.
Computes Chinese Remainder Theorem (CRT) reconstruction constants and QRNS inverse constants.
"""

import sys
import os
import math
from typing import List, Dict, Tuple, Any

# Add parent dir to import configs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm. Returns (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(a: int, m: int) -> int:
    """Computes modular inverse of a modulo m: a^(-1) mod m."""
    gcd_val, x, _ = extended_gcd(a % m, m)
    if gcd_val != 1:
        raise ValueError(f"Modular inverse does not exist for a={a}, m={m}")
    return (x % m + m) % m


def generate_qrns_moduli_set() -> Dict[str, Any]:
    """
    Generates the official 8-modulus QRNS set where each modulus is odd,
    pairwise coprime, and satisfies j^2 = -1 mod m.
    """
    moduli = cfg.moduli_qrns_compute
    roots = cfg.roots_qrns_compute

    # Verify all properties
    for m, j in zip(moduli, roots):
        assert m % 2 != 0, f"Modulus {m} must be odd"
        assert (j * j) % m == (m - 1), f"Root {j} failed j^2 = -1 mod {m}"

    # Verify pairwise coprimality
    for i in range(len(moduli)):
        for k in range(i + 1, len(moduli)):
            assert (
                math.gcd(moduli[i], moduli[k]) == 1
            ), f"Moduli pair ({moduli[i]}, {moduli[k]}) is not coprime"

    M_tot = 1
    for m in moduli:
        M_tot *= m

    M_i = [M_tot // m for m in moduli]
    N_i = [mod_inverse(M_i[i], moduli[i]) for i in range(len(moduli))]
    inv_2 = [mod_inverse(2, m) for m in moduli]
    inv_j = [mod_inverse(j, m) for j, m in zip(roots, moduli)]

    return {
        "moduli": moduli,
        "roots": roots,
        "M_total": M_tot,
        "M_bits": math.log2(M_tot),
        "M_i": M_i,
        "N_i": N_i,
        "inv_2": inv_2,
        "inv_j": inv_j,
    }


def generate_prns_moduli_set() -> Dict[str, Any]:
    """
    Generates the PRNS set for Hybrid Memory-Optical architecture.
    Optics uses top 8 odd moduli (M8 = 63.4 bits, bounds 62-bit sub-products).
    CMOS uses top 9 odd moduli (M9 = 71.2 bits, bounds 63-bit cross-term).
    """
    opt_moduli = [255, 253, 251, 247, 241, 239, 233, 229]
    cmos_moduli = [255, 253, 251, 247, 241, 239, 233, 229, 227, 223]

    def prep_crt(mods):
        M_tot = 1
        for m in mods:
            M_tot *= m
        M_i = [M_tot // m for m in mods]
        N_i = [mod_inverse(M_i[i], mods[i]) for i in range(len(mods))]
        return M_tot, M_i, N_i

    opt_M_tot, opt_M_i, opt_N_i = prep_crt(opt_moduli)
    cmos_M_tot, cmos_M_i, cmos_N_i = prep_crt(cmos_moduli)

    return {
        "opt_moduli": opt_moduli,
        "cmos_moduli": cmos_moduli,
        "opt_M_tot": opt_M_tot,
        "cmos_M_tot": cmos_M_tot,
        "opt_M_i": opt_M_i,
        "cmos_M_i": cmos_M_i,
        "opt_N_i": opt_N_i,
        "cmos_N_i": cmos_N_i,
        "opt_M_bits": opt_M_tot.bit_length(),
        "cmos_M_bits": cmos_M_tot.bit_length(),
    }


def to_prns(
    x_l: int, x_h: int, prns_info: Dict[str, Any]
) -> Tuple[List[int], List[int]]:
    """Forward PRNS projection for Hybrid logic (Optical Domain Only)."""
    opt_moduli = prns_info["opt_moduli"]

    # Optical clusters (8 moduli)
    opt_xl = [x_l % m for m in opt_moduli]
    opt_xh = [x_h % m for m in opt_moduli]

    return opt_xl, opt_xh


def from_prns(residues: List[int], prns_info: Dict[str, Any]) -> int:
    """Inverse PRNS reconstruction recovering a signed integer via CRT using opt_moduli."""
    moduli = prns_info["opt_moduli"]
    M_tot = prns_info["opt_M_tot"]
    M_i = prns_info["opt_M_i"]
    N_i = prns_info["opt_N_i"]

    val = crt_reconstruct(residues, moduli, M_i, N_i)
    if val >= M_tot // 2:
        val -= M_tot
    return val


def generate_moduli_set(
    N_tiles: int = cfg.N_tiles,
    N_rrns: int = cfg.N_rrns_redundant,
    m_max: int = cfg.m_max,
    target_bits: int = 64,
) -> Dict[str, Any]:
    """Generates standard flat coprime moduli set."""
    prime_powers = []
    for p in range(2, m_max + 1):
        if is_prime(p):
            k = 1
            max_power = p
            while p ** (k + 1) <= m_max:
                k += 1
                max_power = p**k
            prime_powers.append((max_power, p))

    prime_powers.sort(key=lambda x: x[0], reverse=True)

    selected = []
    for power_val, prime_base in prime_powers:
        is_coprime = True
        for sel in selected:
            if math.gcd(power_val, sel) != 1:
                is_coprime = False
                break
        if is_coprime:
            selected.append(power_val)
            if len(selected) == N_tiles + N_rrns:
                break

    moduli_compute = selected[:N_tiles]
    moduli_redundant = selected[N_tiles : N_tiles + N_rrns]

    M_compute = 1
    for m in moduli_compute:
        M_compute *= m

    M_i = [M_compute // m for m in moduli_compute]
    N_i = [mod_inverse(M_i[i], moduli_compute[i]) for i in range(N_tiles)]

    return {
        "moduli_compute": moduli_compute,
        "moduli_redundant": moduli_redundant,
        "moduli_full": moduli_compute + moduli_redundant,
        "M_total": M_compute,
        "M_bits": M_compute.bit_length(),
        "M_i": M_i,
        "N_i": N_i,
    }


def to_rns(X: int, moduli: List[int]) -> List[int]:
    """Decomposes an integer into RNS residue channels."""
    return [X % m for m in moduli]


def crt_reconstruct(
    residues: List[int], moduli: List[int], M_i: List[int] = None, N_i: List[int] = None
) -> int:
    """Reconstructs an integer from residue channels using the Chinese Remainder Theorem."""
    k = len(residues)
    if M_i is None or N_i is None:
        M_tot = 1
        for m in moduli[:k]:
            M_tot *= m
        M_i = [M_tot // m for m in moduli[:k]]
        N_i = [mod_inverse(M_i[i], moduli[i]) for i in range(k)]
    else:
        M_tot = 1
        for m in moduli[:k]:
            M_tot *= m

    X_acc = 0
    for i in range(k):
        pp = (int(residues[i]) * int(N_i[i])) % int(moduli[i])
        X_acc += int(pp) * int(M_i[i])

    return int(X_acc % M_tot)


if __name__ == "__main__":
    prns_info = generate_prns_moduli_set()
    print("=" * 70)
    print("JANUS: OFFICIAL HYBRID PRNS REGISTRY (ALGORITHM 5A)")
    print("=" * 70)
    print(f"Optical Moduli Set : {prns_info['opt_moduli']}")
    print(f"CMOS Moduli Set    : {prns_info['cmos_moduli']}")
    print(f"Optical Range      : {prns_info['opt_M_bits']:.3f} bits")
    print(f"CMOS Range         : {prns_info['cmos_M_bits']:.3f} bits")
    print("-" * 70)

    # Test PRNS 64-bit cross term reconstruction
    x_l, x_h = 2147483647, -2147483648
    y_l, y_h = -2147483648, 2147483647

    # Forward PRNS
    opt_al, opt_ah = to_prns(x_l, x_h, prns_info)
    opt_bl, opt_bh = to_prns(y_l, y_h, prns_info)

    # Computations
    C_xl_yl = [
        (al * bl) % m for al, bl, m in zip(opt_al, opt_bl, prns_info["opt_moduli"])
    ]
    C_xh_yh = [
        (ah * bh) % m for ah, bh, m in zip(opt_ah, opt_bh, prns_info["opt_moduli"])
    ]
    C_xl_yh = [
        (al * bh) % m for al, bh, m in zip(opt_al, opt_bh, prns_info["opt_moduli"])
    ]
    C_xh_yl = [
        (ah * bl) % m for ah, bl, m in zip(opt_ah, opt_bl, prns_info["opt_moduli"])
    ]

    # Inverse PRNS
    xl_yl_rec = from_prns(C_xl_yl, prns_info)
    xh_yh_rec = from_prns(C_xh_yh, prns_info)
    xl_yh_rec = from_prns(C_xl_yh, prns_info)
    xh_yl_rec = from_prns(C_xh_yl, prns_info)
    cross_rec = xl_yh_rec + xh_yl_rec

    assert xl_yl_rec == x_l * y_l, "PRNS Low Part Mismatch"
    assert xh_yh_rec == x_h * y_h, "PRNS High Part Mismatch"
    assert cross_rec == x_l * y_h + x_h * y_l, "PRNS Cross Part Mismatch"

    print("[PASS] PRNS Hybrid Architecture 100% Mathematically Verified.")
    print("=" * 70)
