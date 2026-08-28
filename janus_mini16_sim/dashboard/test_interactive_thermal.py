"""
Automated Pytest Suite for Custom Workload JIR Thermal Simulator and Tile Physical Inspector.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tier5_python_rns.jir_thermal_scheduler import JIRThermalScheduler


def test_custom_workload_simulation_low():
    scheduler = JIRThermalScheduler()
    res = scheduler.run_custom_workload_simulation(active_tile_count=4, intensity="low", duration_val=10.0, duration_unit="seconds", jir_enabled=True)

    assert res["active_tile_count"] == 4
    assert res["intensity"] == "low"
    assert res["duration_seconds"] == 10.0
    assert res["max_temperature_C"] <= 70.0  # Must be well below operating ceiling
    assert res["thermal_violations"] == 0
    assert len(res["timeline"]) == 100
    assert len(res["final_temperatures"]) == 16


def test_custom_workload_simulation_critical_stress():
    scheduler = JIRThermalScheduler()
    res = scheduler.run_custom_workload_simulation(active_tile_count=8, intensity="critical", duration_val=1.0, duration_unit="minutes", jir_enabled=True)

    assert res["active_tile_count"] == 8
    assert res["intensity"] == "critical"
    # Even under critical 1.0W stress, JIR rotations must prevent crystallization guard violations (<150 C)
    assert res["max_temperature_C"] < 150.0
    assert len(res["final_temperatures"]) == 16


def test_custom_workload_simulation_jir_disabled_contrast():
    scheduler = JIRThermalScheduler()
    # Run with JIR OFF under high intensity
    res_off = scheduler.run_custom_workload_simulation(
        active_tile_count=4,
        intensity="high",
        duration_val=1.0,
        duration_unit="hours",
        jir_enabled=False
    )
    # Run with JIR ON under high intensity
    res_on = scheduler.run_custom_workload_simulation(
        active_tile_count=4,
        intensity="high",
        duration_val=1.0,
        duration_unit="hours",
        jir_enabled=True
    )

    # JIR OFF must result in higher unmitigated temperature on active tiles compared to JIR ON
    assert res_off["jir_enabled"] is False
    assert res_off["total_rotations_count"] == 0  # 0 swaps when JIR is disabled
    assert res_off["max_temperature_C"] > res_on["max_temperature_C"]
    assert res_on["total_rotations_count"] > 0


def test_tile_detailed_physical_specs():
    scheduler = JIRThermalScheduler()
    specs = scheduler.get_tile_detailed_physical_specs(tile_id=0, temperature_C=45.0, state="ACTIVE")

    assert specs["tile_id"] == 0
    assert specs["modulus"] == 256
    assert specs["temperature_C"] == 45.0
    assert specs["delta_T_K"] == 20.0  # 45 - 25 = 20 K
    assert float(specs["thermo_optic_delta_n"]) > 0
    assert specs["phase_drift_rad"] > 0
    assert specs["crystallization_safety_margin_C"] == 105.0  # 150 - 45 = 105 C margin
    assert specs["operating_limit_margin_C"] == 25.0  # 70 - 45 = 25 C margin
    assert specs["natural_q_dissipated_mW"] > 0
    assert specs["eye_height_V"] > 0
    assert specs["thermal_jitter_ps"] > 0


def test_optical_eye_signal_integrity_scaling():
    scheduler = JIRThermalScheduler()
    # At 25 C (Baseline)
    specs_cold = scheduler.get_tile_detailed_physical_specs(tile_id=0, temperature_C=25.0)
    # At 40 C (JIR Trigger)
    specs_warm = scheduler.get_tile_detailed_physical_specs(tile_id=0, temperature_C=40.0)
    # At 75 C (Hotspot Stress)
    specs_hot = scheduler.get_tile_detailed_physical_specs(tile_id=0, temperature_C=75.0)

    # Eye opening must compress as temperature rises
    assert specs_cold["eye_height_V"] > specs_warm["eye_height_V"] > specs_hot["eye_height_V"]
    # Jitter must increase as temperature rises
    assert specs_cold["thermal_jitter_ps"] < specs_warm["thermal_jitter_ps"] < specs_hot["thermal_jitter_ps"]
    # OSNR must degrade as temperature rises
    assert specs_cold["osnr_dB"] > specs_warm["osnr_dB"] > specs_hot["osnr_dB"]
