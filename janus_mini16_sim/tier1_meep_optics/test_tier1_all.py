"""
Automated Pytest Suite for Tier 0 (GDS Pre-Processor) and Tier 1 (MEEP 3D FDTD Optics).
Verifies Algorithms 0, 1A, 1B, 1C, 1D against strict quantitative design specifications.
"""

import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg
from tier1_meep_optics.gds_layout_processor import GDSLayoutProcessor
from tier1_meep_optics.sb2s3_switch_cell import Sb2S3SwitchCellFDTD
from tier1_meep_optics.waveguide_crossing import WaveguideCrossingFDTD
from tier1_meep_optics.litao3_pockels_router import LiTaO3PockelsModulator
from tier1_meep_optics.export_touchstone import TouchstoneExporter
from tier1_meep_optics.export_heat_map import HeatMapExporter


def test_gds_layout_processor_tier0():
    proc = GDSLayoutProcessor()
    grid = proc.build_grid_domain(10.0, 6.0, 2.0)
    assert grid["total_grid_points"] > 0
    assert grid["dt_fs"] > 0.0
    layers = proc.inspect_layer_table()
    assert layers["LAYER_SI_WG"]["n_complex"] == f"{cfg.n_si} + 0.0j"
    assert layers["LAYER_SIO2_CLAD"]["n_complex"] == f"{cfg.n_sio2} + 0.0j"
    assert layers["LAYER_LITAO3_EO"]["n_complex"] == f"{cfg.n_litao3} + 0.0j"


def test_sb2s3_switch_cell_alg1a():
    solver = Sb2S3SwitchCellFDTD()
    from configs import mini_16t_constants as cfg

    print(
        f"\nk_gst_am: {cfg.get_k_sb2s3('amorphous')}, k_gst_cr: {cfg.get_k_sb2s3('crystalline')}, n_am: {cfg.n_sb2s3_amorph}, n_cr: {cfg.n_sb2s3_cryst}"
    )

    # Amorphous State
    res_am = solver.solve_state("amorphous")
    print("\nAMORPHOUS:", res_am)
    assert res_am["insertion_loss_dB"] <= 0.50
    assert res_am["crosstalk_dB"] <= -20.0
    assert res_am["passivity"] <= 1.0

    # Crystalline State
    res_cr = solver.solve_state("crystalline")
    assert res_cr["insertion_loss_dB"] <= 3.0
    assert res_cr["crosstalk_dB"] <= -8.0
    assert res_cr["passivity"] <= 1.0


def test_waveguide_crossing_alg1b():
    crossing = WaveguideCrossingFDTD()
    res = crossing.solve_crossing()
    assert res["insertion_loss_dB"] <= 0.025
    assert res["crosstalk_dB"] <= -38.0
    assert res["passivity"] <= 1.0001
    assert res["pass_criteria"] is True


def test_litao3_pockels_modulator_alg1c():
    mod = LiTaO3PockelsModulator()
    res = mod.calculate_pockels_effect(V_applied=1.5)
    assert res["V_pi_L_V_cm"] <= 2.0
    assert res["f_EO_bandwidth_GHz"] >= 100.0
    assert res["pass_criteria"] is True


def test_export_touchstone_and_heat_map_alg1d(tmp_path):
    solver = Sb2S3SwitchCellFDTD()
    res = solver.solve_state("amorphous")
    sp = res["S_params"]

    # Construct symmetric 4x4 matrix
    S_mat = np.array(
        [
            [sp["S11"], sp["S21"], sp["S31"], sp["S41"]],
            [sp["S21"], sp["S11"], sp["S41"], sp["S31"]],
            [sp["S31"], sp["S41"], sp["S11"], sp["S21"]],
            [sp["S41"], sp["S31"], sp["S21"], sp["S11"]],
        ],
        dtype=np.complex128,
    )

    # 1. Touchstone Export
    exporter = TouchstoneExporter()
    s4p_path = str(tmp_path / "test_cell.s4p")
    exporter.export_to_file(s4p_path, S_mat)
    assert os.path.exists(s4p_path)

    # 2. HDF5 Heat Map Export
    heat_exporter = HeatMapExporter()
    eps_imag = res["n_complex"].imag * 2 * res["n_complex"].real
    Q_opt = heat_exporter.compute_heat_density(res["E_field_3d"], eps_imag)
    h5_path = str(tmp_path / "test_heat.h5")
    heat_exporter.export_hdf5(
        h5_path, Q_opt, res["spatial_coords"], {"state": "amorphous"}
    )
    assert os.path.exists(h5_path)
    assert np.all(Q_opt >= 0.0)


def test_sb2s3_tolerance_monte_carlo():
    from tier1_meep_optics.sb2s3_tolerance_monte_carlo import (
        run_sb2s3_monte_carlo_tolerance,
    )

    res = run_sb2s3_monte_carlo_tolerance(n_trials=500, seed=42)
    assert res["yield_under_0_5dB_pct"] >= 99.0
    assert res["amorphous_il_mean_dB"] < 0.10
    assert res["crystalline_il_mean_dB"] < 0.20
    assert res["passivity_max"] <= 1.0

