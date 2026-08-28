"""
Automated Pytest Suite for Project JANUS Mini 16-Tile (Tier 5)
Verifies Algorithms 5A through 5F against strict quantitative criteria.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg
from tier5_python_rns.moduli_generator import (
    generate_moduli_set,
    to_rns,
    crt_reconstruct,
)
from tier5_python_rns.formal_verifier import run_formal_verification
from tier5_python_rns.spatial_one_hot_router import SpatialOneHotAccelerator
from tier5_python_rns.jir_thermal_scheduler import JIRThermalScheduler
from tier5_python_rns.rrns_self_healing import RRNSSelfHealingEngine
from tier5_python_rns.gemm_exact_benchmark import run_gemm_precision_benchmark
import numpy as np


def test_moduli_generator_alg5a():
    res = generate_moduli_set()
    assert len(res["moduli_compute"]) == 16
    assert len(res["moduli_redundant"]) == 2
    assert len(res["moduli_full"]) == 18
    assert res["M_bits"] >= 64
    # Test CRT round-trip
    val = 98765432109876543210
    r = to_rns(val, res["moduli_compute"])
    rec = crt_reconstruct(r, res["moduli_compute"], res["M_i"], res["N_i"])
    assert rec == val


def test_z3_formal_verifier_alg5b():
    res = run_formal_verification()
    assert res["all_passed"] is True


def test_spatial_one_hot_router_alg5c():
    acc = SpatialOneHotAccelerator()
    A = np.random.randint(0, 50, size=(cfg.N_dim, cfg.N_dim))
    B = np.random.randint(0, 50, size=(cfg.N_dim, cfg.N_dim))
    C_opt = acc.matmul(A, B)
    C_ref = np.matmul(A.astype(object), B.astype(object))
    diff = int(np.sum(np.abs(C_opt - C_ref)))
    assert diff == 0


def test_jir_thermal_scheduler_alg5d():
    scheduler = JIRThermalScheduler()
    res = scheduler.run_workload_simulation(total_epochs=2000)
    assert res["thermal_violations"] == 0
    assert res["max_temperature_C"] <= cfg.T_max_operating
    assert res["max_temperature_C"] < cfg.T_crystallization_guard


def test_rrns_self_healing_alg5e():
    engine = RRNSSelfHealingEngine()
    res = engine.run_fault_injection_trials(N_trials=2000, error_probability=0.30)
    assert res["detection_rate"] == 1.0
    assert res["correction_rate"] == 1.0
    assert res["false_alarms"] == 0


def test_gemm_exact_benchmark_alg5f():
    res = run_gemm_precision_benchmark(N_dim=cfg.N_dim, precisions=[4, 8, 16, 32, 64])
    for P in [4, 8, 16, 32, 64]:
        assert res[f"INT{P}"]["deviation"] == 0
        assert res[f"INT{P}"]["status"] == "PASS"
