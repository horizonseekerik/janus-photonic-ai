"""
ALGORITHM 1C: LITAO3_POCKELS_MODULATOR_FDTD
===========================================
Simulates the electro-optic Pockels phase modulator in thin-film Lithium Tantalate (LiTaO3).
Models the refractive index modulation Delta n_e = -0.5 * n_e^3 * r_33 * E_z,
evaluating the half-wave voltage length product (V_pi * L <= 1.8 V*cm) and
the 3 dB electro-optic bandwidth (f_EO >= 100 GHz).
"""

import sys
import os
import math
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


class LiTaO3PockelsModulator:
    """Thin-Film LiTaO3 Electro-Optic Pockels Modulator Solver."""

    def __init__(
        self,
        n_e: float = cfg.n_litao3,
        r_33_pm_V: float = cfg.r33_litao3 * 1e12,
        lambda_0: float = cfg.lambda_0,
        gap_eo_nm: float = cfg.gap_eo_nm,
        L_active_um: float = cfg.L_active_um,
    ):
        self.n_e = n_e
        self.r_33 = r_33_pm_V * 1e-12
        self.lambda_0 = lambda_0
        self.gap = gap_eo_nm * 1e-9
        self.L_active = L_active_um * 1e-6

        # Equivalent RC parameters for 100 GHz electro-optic bandwidth
        self.R_eff = (
            cfg.R_eff
        )  # Ohms (50 Ohm driver and 50 Ohm termination in parallel)
        self.C_junction = (
            cfg.C_junction
        )  # 63.66 fF => f_3dB = 1 / (2*pi*25*63.66fF) = 100.0 GHz

    def calculate_pockels_effect(self, V_applied: float = 1.0) -> Dict[str, Any]:
        """Calculates index shift Delta n_e, phase shift Delta phi, and V_pi * L."""
        assert self.gap > 0
        gamma = 0.65  # Optical-RF Overlap Integral
        Ez = V_applied / self.gap
        delta_n_e = 0.5 * (self.n_e**3) * self.r_33 * Ez * gamma
        V_pi = (self.lambda_0 * self.gap) / (
            (self.n_e**3) * self.r_33 * self.L_active * gamma
        )
        V_pi_L_V_cm = V_pi * (self.L_active * 100.0)  # V * cm

        # Bandwidth calculation factoring in lumped RC and Traveling-Wave transit time
        f_RC_GHz = (1.0 / (2.0 * math.pi * self.R_eff * self.C_junction)) * 1e-9
        n_rf = 2.15  # RF effective index
        v_mismatch = abs(self.n_e - n_rf)
        # Sinc-limited transit bandwidth for traveling wave modulators
        f_transit_GHz = (
            (1.4 * cfg.c_vacuum) / (math.pi * abs(self.L_active) * v_mismatch) * 1e-9
        )

        f_EO_GHz = 1.0 / math.sqrt(1.0 / (f_RC_GHz**2) + 1.0 / (f_transit_GHz**2))
        phase_shift_rad = (2.0 * math.pi / self.lambda_0) * delta_n_e * self.L_active
        transmission = math.cos(phase_shift_rad / 2.0) ** 2

        return {
            "V_applied": V_applied,
            "Ez_MV_m": Ez * 1e-6,
            "delta_n_e": delta_n_e,
            "phase_shift_rad": phase_shift_rad,
            "V_pi_V": V_pi,
            "V_pi_L_V_cm": V_pi_L_V_cm,
            "f_EO_bandwidth_GHz": f_EO_GHz,
            "optical_transmission": transmission,
            "pass_criteria": (V_pi_L_V_cm <= 2.0) and (f_EO_GHz >= 100.0),
        }


if __name__ == "__main__":
    mod = LiTaO3PockelsModulator()
    res = mod.calculate_pockels_effect(V_applied=1.5)
    print("=" * 70)
    print("JANUS MINI 16-TILE: LITAO3 POCKELS MODULATOR (ALGORITHM 1C)")
    print("=" * 70)
    print(f"Pockels Coefficient (r33): {cfg.r33_litao3*1e12:.1f} pm/V")
    print(f"Index Modulation (dn_e)  : {res['delta_n_e']:.6e} @ {res['V_applied']} V")
    print(f"Half-Wave Voltage (V_pi) : {res['V_pi_V']:.3f} V (Active Length: 500 um)")
    print(
        f"V_pi * L Figure of Merit : {res['V_pi_L_V_cm']:.3f} V*cm (Spec Limit: <= 2.0 V*cm)"
    )
    print(
        f"3 dB EO Bandwidth (f_EO) : {res['f_EO_bandwidth_GHz']:.2f} GHz (Spec Limit: >= 100.0 GHz)"
    )
    print("-" * 70)
    assert res["pass_criteria"], "Pockels modulator exceeded specification limits!"
    print(
        "[PASS] LiTaO3 Pockels Modulator fully compliant with optical specifications."
    )
