"""
PROJECT JANUS MINI (16-TILE): TIER 5 PYTHON RNS ENGINE
======================================================
This package provides the complete mathematical and architectural validation
suite for the JANUS Mini 16-Tile Planar MVP, strictly implementing Algorithms 5A-5F.

Exported Public API:
-------------------
- Algorithm 5A: generate_moduli_set, to_rns, crt_reconstruct
- Algorithm 5B: run_formal_verification
- Algorithm 5C: SpatialOneHotAccelerator, SpatialOneHotTile
- Algorithm 5D: JIRThermalScheduler
- Algorithm 5E: RRNSSelfHealingEngine
- Algorithm 5F: run_gemm_precision_benchmark
"""

from .moduli_generator import (
    generate_moduli_set,
    to_rns,
    crt_reconstruct,
    mod_inverse,
    extended_gcd,
)

from .formal_verifier import (
    run_formal_verification,
    prove_pairwise_coprimality,
    prove_dynamic_range,
)

from .spatial_one_hot_router import SpatialOneHotAccelerator, SpatialOneHotTile

from .jir_thermal_scheduler import JIRThermalScheduler

from .rrns_self_healing import RRNSSelfHealingEngine

from .gemm_exact_benchmark import run_gemm_precision_benchmark

__all__ = [
    # Algorithm 5A
    "generate_moduli_set",
    "to_rns",
    "crt_reconstruct",
    "mod_inverse",
    "extended_gcd",
    # Algorithm 5B
    "run_formal_verification",
    "prove_pairwise_coprimality",
    "prove_dynamic_range",
    "",
    # Algorithm 5C
    "SpatialOneHotAccelerator",
    "SpatialOneHotTile",
    # Algorithm 5D
    "JIRThermalScheduler",
    # Algorithm 5E",
    "RRNSSelfHealingEngine",
    # Algorithm 5F
    "run_gemm_precision_benchmark",
]

__version__ = "1.0.0"
__tier__ = "Tier 5: Architecture, JIR & RNS Arithmetic"
