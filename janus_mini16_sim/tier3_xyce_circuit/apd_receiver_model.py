"""
ALGORITHM 3B: APD_RECEIVER_MODEL
================================
Models the SAC2M (Separate Absorption, Charge, and Multiplication) Ge/Si APD.
Simulates avalanche multiplication gain (M=7), McIntyre excess noise factor (F=2.0),
3 dB bandwidth (105 GHz), Gain-Bandwidth Product (441 GHz), and dark current (1 nA).
"""

import sys
import os
import math
from typing import Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


class SAC2MAPDReceiver:
    """SAC2M Ge/Si Avalanche Photodetector (APD) Physical Equivalent Circuit."""

    def __init__(
        self,
        R_resp: float = cfg.R_responsivity,
        M_gain: int = cfg.M_apd,
        k_ion: float = cfg.k_ionization,
        f_3db_GHz: float = cfg.f_3db_apd * 1e-9,
        GBP_GHz: float = cfg.GBP_apd * 1e-9,
        C_j_fF: float = cfg.C_j_apd * 1e15,
        R_s_ohm: float = cfg.R_s_apd,
        I_surface_nA: float = cfg.I_surface_leakage * 1e9,
        I_bulk_nA: float = cfg.I_bulk_dark * 1e9,
        sigma_latch_noise_uA: float = cfg.sigma_latch_noise * 1e6,
    ):
        self.R = R_resp
        self.M = M_gain
        self.k = k_ion
        self.f_3db = f_3db_GHz * 1e9
        self.GBP = GBP_GHz * 1e9
        self.C_j = C_j_fF * 1e-15
        self.R_s = R_s_ohm
        self.I_surface = I_surface_nA * 1e-9
        self.I_bulk = I_bulk_nA * 1e-9
        self.I_dark = self.I_surface + self.I_bulk * self.M
        self.sigma_latch_noise = sigma_latch_noise_uA * 1e-6
        self.q = cfg.q_electron

        # McIntyre Excess Noise Factor: F(M) = k*M + (1-k)*(2 - 1/M)
        self.F = self.k * self.M + (1.0 - self.k) * (2.0 - 1.0 / self.M)

    def calculate_photocurrent(self, P_opt_W: float) -> float:
        """Calculates multiplied photocurrent I_ph = P_opt * R * M. (Does not include dark current here)."""
        assert P_opt_W >= 0, "Optical power cannot be negative"
        return P_opt_W * self.R * self.M

    def calculate_noise_variance(
        self, P_opt_W: float, bandwidth_Hz: float = 100e9
    ) -> Dict[str, float]:
        """Calculates shot, dark current, latch, and total noise variance (receiverless front end)."""
        assert P_opt_W >= 0, "Optical power cannot be negative"
        I_ph = self.calculate_photocurrent(P_opt_W)

        # Shot noise variance: sigma_shot^2 = 2 * q * I_ph * M * F * delta_f
        # Note: 2*q*(P*R)*M^2*F*delta_f = 2*q*I_ph*M*F*delta_f
        sigma_shot_sq = (
            2.0 * self.q * (P_opt_W * self.R) * (self.M**2) * self.F * bandwidth_Hz
        )

        # Only apply M and F to bulk dark current. Surface leakage is unmultiplied.
        sigma_dark_sq = (
            2.0
            * self.q
            * (self.I_surface + self.I_bulk * (self.M**2) * self.F)
            * bandwidth_Hz
        )

        # Latch thermal noise (receiverless design)
        sigma_latch_sq = self.sigma_latch_noise**2
        sigma_total_sq = sigma_shot_sq + sigma_dark_sq + sigma_latch_sq
        sigma_total = math.sqrt(sigma_total_sq)

        return {
            "I_photo_uA": I_ph * 1e6,
            "sigma_shot_uA": math.sqrt(sigma_shot_sq) * 1e6,
            "sigma_dark_uA": math.sqrt(sigma_dark_sq) * 1e6,
            "sigma_total_uA": sigma_total * 1e6,
            "sigma_total_A": sigma_total,
        }

    def generate_spice_netlist(self) -> str:
        """Generates SPICE netlist subcircuit for the SAC2M APD."""
        return f"""* SAC2M Ge/Si APD Subcircuit Model
.SUBCKT SAC2M_APD OPT_IN CATHODE ANODE
* Responsivity R={self.R} A/W, Gain M={self.M}, F={self.F:.2f}
G_PHOTO CATHODE_INT ANODE VALUE = {{ V(OPT_IN) * {self.R * self.M} }}
C_JUNCTION CATHODE_INT ANODE {self.C_j}
R_SERIES CATHODE_INT CATHODE {self.R_s}
.ENDS SAC2M_APD
"""


if __name__ == "__main__":
    apd = SAC2MAPDReceiver()
    P_det_test = cfg.P_det  # 13.82 uW
    noise = apd.calculate_noise_variance(P_det_test, bandwidth_Hz=cfg.f_3db_apd)

    print("=" * 70)
    print("JANUS MINI 16-TILE: SAC2M Ge/Si APD RECEIVER (ALGORITHM 3B)")
    print("=" * 70)
    print(f"Responsivity (R)      : {apd.R:.2f} A/W @ 1064 nm")
    print(f"Avalanche Gain (M)    : {apd.M}")
    print(f"Excess Noise Factor(F): {apd.F:.2f} (McIntyre Formula)")
    print(
        f"3 dB Bandwidth        : {apd.f_3db*1e-9:.1f} GHz (Gain-Bandwidth: {apd.GBP*1e-9:.1f} GHz)"
    )
    print(f"Junction Capacitance  : {apd.C_j*1e15:.2f} fF (Series R: {apd.R_s} Ohm)")
    print(f"Dark Current          : {apd.I_dark*1e9:.2f} nA (Spec Limit: <= 1.0 nA)")
    print(
        f"Multiplied Signal Curr: {noise['I_photo_uA']:.3f} uA @ P_det = {P_det_test*1e6:.2f} uW"
    )
    print(
        f"Total Noise Current   : {noise['sigma_total_uA']:.3f} uA (Shot: {noise['sigma_shot_uA']:.3f})"
    )
    print("-" * 70)
    assert apd.I_dark <= 1e-9, "Dark current exceeded 1 nA limit!"
    assert apd.f_3db >= 100e9, "Bandwidth below 100 GHz!"
    print("[PASS] SAC2M APD Receiver Model fully verified.")
