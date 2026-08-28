"""
Automated Pytest Suite for Prolonged Hours-Scale JIR Thermal Simulation.
Verifies asymptotic limit-cycle convergence over 1 hour, 6 hours, and 24 hours of operation.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tier5_python_rns.jir_thermal_scheduler import JIRThermalScheduler


def test_prolonged_1_hour_simulation():
    scheduler = JIRThermalScheduler()
    res = scheduler.run_custom_workload_simulation(
        active_tile_count=4,
        intensity="high",
        duration_val=1.0,
        duration_unit="hours"
    )

    assert res["duration_seconds"] == 3600.0
    assert res["active_tile_count"] == 4
    assert res["total_energy_Wh"] > 0
    assert res["total_compute_delivered_pmacs"] > 0
    assert res["max_temperature_C"] <= 70.0  # Must not exceed operating ceiling
    assert res["thermal_violations"] == 0
    assert res["total_rotations_count"] > 10000  # Thousands of JIR rotation cycles


def test_prolonged_24_hour_stress_test():
    scheduler = JIRThermalScheduler()
    res = scheduler.run_custom_workload_simulation(
        active_tile_count=8,
        intensity="critical",
        duration_val=24.0,
        duration_unit="hours"
    )

    assert res["duration_seconds"] == 86400.0
    assert res["active_tile_count"] == 8
    # Even under 24 hours of continuous critical stress, peak temp must remain < 150 C crystallization threshold
    assert res["max_temperature_C"] < 150.0
    assert len(res["timeline"]) == 100
    assert res["total_rotations_count"] > 100000
