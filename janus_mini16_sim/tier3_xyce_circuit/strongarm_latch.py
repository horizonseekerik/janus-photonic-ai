"""
ALGORITHM 3C: STRONGARM_LATCH
=============================
Models the 100 GHz StrongARM regenerative decision latch.
Evaluates regeneration time (t_regen = 3.5 ps <= 4.0 ps), dynamic decision energy
(E_decision = 100 aJ), and resolves binary decisions under receiver noise floors.
"""

import sys
import os
import math
import numpy as np
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


class StrongARMLatch:
    """100 GHz Dual-Rail Regenerative Dynamic StrongARM Comparator."""

    def __init__(
        self,
        t_regen_ps: float = cfg.t_regen * 1e12,
        E_decision_aJ: float = cfg.E_strongarm * 1e18,
        V_dd: float = 0.8,
        sigma_latch_noise_uA: float = cfg.sigma_latch_noise * 1e6,
    ):
        self.t_regen = t_regen_ps * 1e-12  # 3.5 ps
        self.E_decision = E_decision_aJ * 1e-18  # 100 aJ
        self.V_dd = V_dd
        self.sigma_latch_noise = sigma_latch_noise_uA * 1e-6

        # Equivalent transconductance and regenerative load capacitance
        # t_regen = (C_load / g_m) * ln(V_dd / V_diff)
        # Active node capacitance is ~20% of total dynamic capacitance
        self.C_load = (self.E_decision / (self.V_dd**2)) * 0.2  # ~31.25 aF
        self.g_m = cfg.g_m_latch

        # Receiverless front-end: the differential current is never converted to a
        # voltage via a transimpedance resistor. Instead it dumps charge directly
        # onto the sensing-node parasitic capacitance (mandated exactly 5 fF) for
        # a fixed integration window, and THAT charge sets the initial regen voltage.
        self.C_p = cfg.C_p_strongarm  # 5.0 fF, exact per spec
        self.t_int = cfg.t_int_strongarm  # integration window before regen kicks in

    def simulate_decision(
        self, I_diff_A: float, noise_sigma_A: float
    ) -> Dict[str, Any]:
        """
        Simulates dynamic latch decision under differential input current and Gaussian noise.
        The front end is receiverless: no transimpedance stage. Differential current
        integrates as charge onto the 5 fF sensing-node capacitance over t_int, and the
        resulting voltage (Q = I*t, V = Q/C_p) seeds the regenerative StrongARM core.
        Returns binary decision (0 or 1), regeneration latency, and energy dissipation.
        """
        # Add random noise sample
        sampled_noise = np.random.normal(0, noise_sigma_A)
        net_diff_current = I_diff_A + sampled_noise

        # Charge-integration front end (receiverless): V = I * t_int / C_p
        V_diff = max(abs(net_diff_current) * self.t_int / self.C_p, 1e-6)
        V_diff = min(V_diff, self.V_dd * 0.99)

        # Total latency = Integration + Linear Regeneration + Non-linear Slew
        I_tail = 400e-6  # 400 uA tail current
        t_integration = self.C_load * (self.V_dd / 3.0) / I_tail
        tau_lat = self.C_load / self.g_m
        t_linear_regen = tau_lat * math.log(self.V_dd / V_diff)
        t_slew = 1.0e-12  # Slew time
        t_total_delay = t_integration + t_linear_regen + t_slew

        t_setup = getattr(cfg, "t_setup", 1e-12)
        if t_total_delay > (cfg.T_cycle - t_setup):
            # Metastability: Random decision
            decision = np.random.randint(0, 2)
        else:
            decision = 1 if net_diff_current > 0 else 0

        return {
            "I_diff_uA": I_diff_A * 1e6,
            "net_diff_uA": net_diff_current * 1e6,
            "decision": decision,
            "t_regen_ps": t_total_delay * 1e12,
            "E_decision_aJ": self.E_decision * 1e18,
            "pass_regen_time": t_total_delay <= 4.0e-12,
        }


if __name__ == "__main__":
    latch = StrongARMLatch()
    res = latch.simulate_decision(I_diff_A=50e-6, noise_sigma_A=cfg.sigma_latch_noise)

    print("=" * 70)
    print("JANUS MINI 16-TILE: STRONGARM REGENERATIVE LATCH (ALGORITHM 3C)")
    print("=" * 70)
    print(f"Supply Voltage (V_DD)  : {latch.V_dd:.2f} V")
    print(
        f"Regeneration Time      : {res['t_regen_ps']:.2f} ps (Spec Limit: <= 4.0 ps)"
    )
    print(
        f"Decision Energy        : {res['E_decision_aJ']:.1f} aJ (Spec Target: 100 aJ)"
    )
    print(
        f"Decision Output        : Bit={res['decision']} (Net Diff Current={res['net_diff_uA']:.2f} uA)"
    )
    print("-" * 70)
    assert res["pass_regen_time"], "Regeneration time exceeded 4.0 ps threshold!"
    print("[PASS] StrongARM Regenerative Latch validated for 100 GHz operation.")
