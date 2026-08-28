"""
Automated Pytest Suite for Tier 3 (Xyce Circuit & Signal Integrity).
Verifies Algorithms 3A, 3B, 3C, 3D, 3E against strict electrical and SI limits.
"""

import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg
from tier3_xyce_circuit.vector_fit_s_params import VectorFitSParams
from tier3_xyce_circuit.apd_receiver_model import SAC2MAPDReceiver
from tier3_xyce_circuit.strongarm_latch import StrongARMLatch
from tier3_xyce_circuit.eye_diagram_ber import EyeDiagramAndBERSolver
from tier3_xyce_circuit.ilo_comb_lock import ILOFrequencyCombLock


def test_vector_fit_s_params_alg3a():
    # Symmetric 4x4 matrix
    S_mat = np.eye(4, dtype=np.complex128) * 0.9
    vfit = VectorFitSParams(num_poles=4)
    res = vfit.fit_s_matrix(S_mat)

    assert res["is_stable"] is True
    assert res["max_passivity"] <= 1.0001
    assert res["pass_criteria"] is True

    cir_text = vfit.generate_spice_subcircuit(res)
    assert ".SUBCKT OPTICAL_SWITCH_4PORT" in cir_text
    assert ".ENDS OPTICAL_SWITCH_4PORT" in cir_text


def test_apd_receiver_model_alg3b():
    apd = SAC2MAPDReceiver()
    assert apd.R == 0.8
    assert apd.M == 7
    assert abs(apd.F - cfg.F_excess_noise) <= 0.25
    assert apd.f_3db >= 100e9
    assert apd.I_dark <= 1e-9

    noise = apd.calculate_noise_variance(cfg.P_det)
    assert noise["I_photo_uA"] > 0.0
    assert noise["sigma_total_uA"] > 0.0


def test_strongarm_latch_alg3c():
    latch = StrongARMLatch()
    res = latch.simulate_decision(I_diff_A=50e-6, noise_sigma_A=cfg.sigma_latch_noise)

    assert res["t_regen_ps"] <= 4.0
    assert res["E_decision_aJ"] <= 120.0
    assert res["pass_regen_time"] is True
    assert res["decision"] in [0, 1]


def test_eye_diagram_and_ber_alg3d_3e():
    np.random.seed(42)
    solver = EyeDiagramAndBERSolver()
    res = solver.calculate_link_budget_and_ber()

    assert res["link_margin_dB"] >= 3.0
    assert res["Q_factor"] >= 9.38
    assert res["pass_margin"] is True
    assert res["pass_Q"] is True
    assert res["pass_BER"] is True

    eye = solver.generate_100ghz_eye_trace(num_bits=5000)
    print("EYE TRACE:", eye)
    assert eye["eye_opening_pct"] >= 25.4
    assert eye["pass_eye_opening"] is True

    # Reconciled Q-Factor assertion: both analytic and time-domain Q must satisfy Q >= 9.38
    q_analytic = res["Q_factor"]
    q_time_domain = eye["time_domain_Q"]
    assert q_time_domain >= 9.38, f"Time-domain Q {q_time_domain:.2f} fell below 9.38 threshold!"
    q_diff_pct = abs(q_analytic - q_time_domain) / q_analytic * 100.0
    print(f"Q-factor Analytic: {q_analytic:.2f}, Time-Domain: {q_time_domain:.2f}, Diff: {q_diff_pct:.2f}%")
    assert q_diff_pct <= 18.0, f"Q-factor discrepancy {q_diff_pct:.2f}% exceeds tolerance!"


def test_ilo_comb_lock_alg3f():
    ilo = ILOFrequencyCombLock()
    trans_res = ilo.simulate_phase_locking_transient(delta_f0_Hz=150e6)
    jitter_res = ilo.calculate_phase_noise_and_jitter()

    assert trans_res["is_locked"] is True
    assert trans_res["f_lock_bandwidth_GHz"] >= 0.5  # Lock bandwidth >= 500 MHz
    assert trans_res["phase_error_rad"] <= 0.15
    assert jitter_res["pass_jitter_budget"] is True
    assert jitter_res["sigma_t_fs"] <= 50.0
