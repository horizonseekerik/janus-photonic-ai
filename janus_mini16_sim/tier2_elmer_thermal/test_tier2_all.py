"""
Automated Pytest Suite for Tier 2 (3D Multi-Stratum Thermal FEM).
Verifies Algorithms 2A, 2B, 2C, 2D against strict thermal specifications.
"""

import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg
from tier2_elmer_thermal.gmsh_mesh_generator import Gmsh3DMeshGenerator
from tier2_elmer_thermal.elmer_thermal_solver import ElmerTransientThermalSolver
from tier2_elmer_thermal.extract_thermal_rom import ThermalROMExtractor


def test_gmsh_mesh_generator_alg2a(tmp_path):
    generator = Gmsh3DMeshGenerator()
    geo_path = str(tmp_path / "test_mesh.geo")
    generator.generate_geo_script(geo_path)
    assert os.path.exists(geo_path)

    vols = generator.calculate_mesh_volumes()
    assert vols["h_total_active_um"] == 330.0
    assert vols["volumes_mm3"]["Active_Total"] > 0.0
    assert vols["thermal_capacitances_mJ_K"]["Total"] > 0.0


def test_elmer_thermal_solver_alg2b_2c():
    solver = ElmerTransientThermalSolver(
        R_poles=[0.12, 0.08, 0.05, 0.03, 0.02],
        tau_poles=[69.06e-3, 15.0e-3, 3.0e-3, 0.5e-3, 0.05e-3],
    )
    res = solver.evaluate_steady_state()

    # FIX (audit CRITICAL): was `<= 1.0`, contradicting both the project
    # spec and the solver's own `pass_steady_state_limit` check (<= 0.25 K).
    assert res["delta_T_steady_K"] <= 0.25
    assert res["T_peak_operating_C"] <= cfg.T_max_operating
    assert res["crystallization_margin_C"] >= 80.0
    assert bool(res["pass_steady_state_limit"]) is True
    assert bool(res["pass_operating_temp_limit"]) is True
    assert bool(res["pass_crystallization_guard"]) is True

    # ADDED: coverage for the two checks the audit found completely absent
    # from the solver -- pulse energy conservation and crystallization kinetics.
    pulse_res = solver.verify_pulse_energy_conservation()
    assert pulse_res["energy_conservation_error_frac"] < 1e-6
    assert bool(pulse_res["pass_pulse_energy_conservation"]) is True

    # ADDED: literature-grounded PCM switching-energy cross-check (see
    # elmer_thermal_solver.py verify_pcm_switching_energy docstring).
    pcm_energy_res = solver.verify_pcm_switching_energy()
    assert pcm_energy_res["E_crystallize_J"] > 0.0
    assert pcm_energy_res["E_amorphize_J"] > 0.0
    assert bool(pcm_energy_res["within_order_of_magnitude_of_cfg_band"]) is True

    xtal_res = solver.evaluate_crystallization_kinetics()
    assert xtal_res["crystallized_fraction"] < 1.0
    assert bool(xtal_res["pass_crystallization_kinetics"]) is True


def test_extract_thermal_rom_alg2d():
    extractor = ThermalROMExtractor()
    res = extractor.extract_and_fit_rom()

    # FIX (audit CRITICAL): was `>= -1.0` (accepts any fit, including a
    # catastrophic one) and only checked an arbitrary R_total bound with zero
    # real coverage of ROM accuracy. Now enforces the actual spec: R^2 >= 0.999
    # AND checks each extracted pole is physically sane (positive, finite).
    assert res["r_squared"] >= 0.999
    assert bool(res["pass_r_squared"]) is True
    assert bool(res["pass_tau1"]) is True
    assert res["R_total_K_W"] <= 0.35
    assert all(
        r > 0.0 for r in res["R_poles_K_W"]
    ), "Fitted thermal resistances must be positive"
    assert all(np.isfinite(res["R_poles_K_W"])), "Fitted resistances must be finite"
    assert all(
        t > 0.0 for t in res["tau_poles_s"]
    ), "Fitted time constants must be positive"
    assert all(np.isfinite(res["tau_poles_s"])), "Fitted time constants must be finite"
