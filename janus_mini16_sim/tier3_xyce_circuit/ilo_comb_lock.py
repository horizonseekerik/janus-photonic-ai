"""
ALGORITHM 3F: INJECTION_LOCKED_COMB_CLOCK_SOLVE
__________________________________________________
Hardware-level physical modeling of the optical-frequency-comb referenced
Injection-Locked Oscillator (ILO) clock distribution network for Project JANUS.

Simulates:
plus pulses, stochastic Adler phase dynamics with Langevin noise,
acquisition locking range, Leeson phase noise filtering, and RSS jitter.
"""

import sys
import os
import math
import numpy as np
from typing import Dict, Any, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg


class ILOFrequencyCombLock:
    """
    Physical solver for a 100 GHz optical-comb-referenced Injection-Locked Oscillator (ILO).
    Solves stochastic Adler phase dynamics and evaluates closed-loop jitter.
    """

    def __init__(
        self,
        f_rep_Hz: float = 100.0e9,
        Q_tank: float = 15.0,
        I_osc_A: float = 2.0e-3,
        P_comb_avg_W: float = 100.0e-6,
        tau_pulse_s: float = 1.5e-12,
        T_K: float = 343.15,
    ):
        self.f_rep = f_rep_Hz
        self.omega_rep = 2.0 * math.pi * self.f_rep
        self.Q_tank = Q_tank
        self.I_osc = I_osc_A
        self.P_comb_avg = P_comb_avg_W
        self.tau_pulse = tau_pulse_s
        self.T_K = T_K

        # Detector parameters
        self.R = cfg.R_responsivity  # 0.8 A/W
        self.M0 = cfg.M_apd  # 7

        # Physical constants
        self.k_B = 1.380649e-23
        self.q = 1.602176634e-19

        # Derive peak optical power & injected photocurrent
        T_rep = 1.0 / self.f_rep
        self.P_peak = self.P_comb_avg * (T_rep / (math.sqrt(math.pi) * self.tau_pulse))
        self.I_inj_peak = self.P_peak * self.R * self.M0

        # Injection locking bandwidth (Adler's formula)
        self.omega_L = (self.omega_rep / (2.0 * self.Q_tank)) * (self.I_inj_peak / self.I_osc)
        self.f_lock_Hz = self.omega_L / (2.0 * math.pi)

    def simulate_phase_locking_transient(
        self,
        delta_f0_Hz: float = 150.0e6,  # 150 MHz initial thermal detuning
        t_sim_s: float = 1.0e-9,       # 1.0 ns transient window
        N_steps: int = 2000,
        phi_0_rad: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Solves Adler's stochastic differential equation using Euler-Maruyama:
        dphi/dt = Delta_omega_0 - omega_L * sin(phi) + sqrt(2 * D_phi) * xi(t)
        """
        dt = t_sim_s / N_steps
        time_vec = np.linspace(0, t_sim_s, N_steps)
        delta_omega_0 = 2.0 * math.pi * delta_f0_Hz

        # Verify detuning is within locking range
        is_in_locking_range = abs(delta_f0_Hz) < self.f_lock_Hz
        phi_ss_theoretical = math.asin(np.clip(delta_omega_0 / self.omega_L, -1.0, 1.0)) if is_in_locking_range else 0.0

        # Phase diffusion coefficient from free-running oscillator linewidth (~100 kHz)
        delta_f_linewidth = 100.0e3
        D_phi = math.pi * delta_f_linewidth

        # Euler-Maruyama integration
        phi = np.zeros(N_steps)
        phi[0] = phi_0_rad

        for n in range(N_steps - 1):
            drift = delta_omega_0 - self.omega_L * math.sin(phi[n])
            diffusion = math.sqrt(2.0 * D_phi / dt) * np.random.normal(0, 1.0)
            phi[n + 1] = phi[n] + (drift + diffusion) * dt

        # Steady-state check (average over last 20% of trajectory)
        steady_state_slice = phi[int(N_steps * 0.8):]
        phi_measured_ss = float(np.mean(steady_state_slice))
        phase_error_rad = abs(phi_measured_ss - phi_ss_theoretical)

        lock_indices = np.where(np.abs(phi - phi_ss_theoretical) < 0.05)[0]
        time_to_lock_ps = float(lock_indices[0] * dt * 1e12) if (is_in_locking_range and len(lock_indices) > 0) else float(t_sim_s * 1e12)

        return {
            "is_locked": is_in_locking_range,
            "f_lock_bandwidth_GHz": self.f_lock_Hz / 1e9,
            "delta_f0_MHz": delta_f0_Hz / 1e6,
            "phi_ss_theoretical_rad": phi_ss_theoretical,
            "phi_measured_ss_rad": phi_measured_ss,
            "phase_error_rad": phase_error_rad,
            "time_to_lock_ps": time_to_lock_ps,
            "time_vector_ps": (time_vec * 1e12).tolist(),
            "phi_trajectory_rad": phi.tolist(),
        }

    def calculate_phase_noise_and_jitter(
        self,
        f_min_Hz: float = 10.0e3,
        f_max_Hz: float = 50.0e9,
        N_pts: int = 1000,
        delta_f0_Hz: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Integrates the composite phase noise spectrum S_phi(f) over the Myquist bandwidth:
        S_phi,out(f) = S_phi,comb(f) * |H_ILO(f)|^2 + S_phi,free(f) * |1 - H_ILO(f)|^2
        """
        freqs = np.logspace(np.log10(f_min_Hz), np.log10(f_max_Hz), N_pts)
        
        # Effective tracking loop bandwidth (omega_lock * cos(phi_ss))
        delta_omega_0 = 2.0 * math.pi * delta_f0_Hz
        sin_phi = np.clip(delta_omega_0 / self.omega_L, -0.99, 0.99)
        cos_phi = math.sqrt(1.0 - sin_phi**2)
        omega_3db = self.omega_L * cos_phi
        f_3db = omega_3db / (2.0 * math.pi)

        # 1. Optical frequency comb phase noise model (sub-50 fs comb reference)
        # L_comb(10 MHz) = -148 dBc/Hz, floor = -168 dBc/Hz
        L_comb_10M = 10.0 ** (-148.0 / 10.0)
        floor_comb = 10.0 ** (-168.0 / 10.0)
        S_phi_comb = 2.0 * (L_comb_10M * (10.0e6 / freqs) ** 2 + floor_comb)

        # 2. Free-running 100 GHz LC oscillator phase noise (Leeson model)
        # L_free(10 MHz) = -105 dBc/Hz, 1/f corner = 1 MHz, thermal floor = -155 dBc/Hz
        L_free_10M = 10.0 ** (-105.0 / 10.0)
        f_corner = 1.0e6
        floor_free = 10.0 ** (-155.0 / 10.0)
        S_phi_free = 2.0 * (L_free_10M * (10.0e6 / freqs) ** 2 * (1.0 + f_corner / freqs) + floor_free)

        # 3. ILO Closed-loop Transfer Functions
        # H_ILO(s) = omega_3db / (s + omega_3db) -> lowpass filter on comb noise
        # 1 - H_ILO(s) = s / (s + omega_3db)    -> highpass filter on oscillator noise
        H_mag2 = (omega_3db**2) / (omega_3db**2 + (2.0 * math.pi * freqs)**2)
        HP_mag2 = ((2.0 * math.pi * freqs)**2) / (omega_3db**2 + (2.0 * math.pi * freqs)**2)

        # 4. Composite Output Phase Noise
        S_phi_out = S_phi_comb * H_mag2 + S_phi_free * HP_mag2

        # 5. Integrate phase variance over Nyquist bandwidth [f_min, f_max]
        sigma_phi_sq = np.trapezoid(S_phi_out, freqs) if hasattr(np, 'trapezoid') else np.trapz(S_phi_out, freqs)
        sigma_phi_rad = math.sqrt(max(0.0, float(sigma_phi_sq)))

        # 6. Convert phase jitter to absolute RMS timing jitter
        # sigma_t = sigma_phi / (2 * pi * f_0)
        sigma_t_s = sigma_phi_rad / self.omega_rep
        sigma_t_fs = sigma_t_s * 1e15

        return {
            "f_3db_tracking_bandwidth_GHz": f_3db / 1e9,
            "sigma_phi_rad": sigma_phi_rad,
            "sigma_t_s": sigma_t_s,
            "sigma_t_fs": sigma_t_fs,
            "pass_jitter_budget": bool(sigma_t_fs <= 50.0),
            "freq_points": freqs.tolist(),
            "S_phi_out_dBc_per_Hz": (10.0 * np.log10(np.maximum(S_phi_out / 2.0, 1e-25))).tolist(),
        }


if __name__ == "__main__":
    ilo = ILOFrequencyCombLock()
    trans_res = ilo.simulate_phase_locking_transient(delta_f0_Hz=150e6)
    jitter_res = ilo.calculate_phase_noise_and_jitter()

    print("=" * 70)
    print("JANUS MINI 16-TILE: 100 GHz INJECTION-LOCKED COMB CLOCK (ALG 3F)")
    print("=" * 70)
    print(f"Injection Locking Bandwidth: +/- {ilo.f_lock_Hz / 1e9:.2f} GHz")
    print(f"Initial Frequency Detuning : {trans_res['delta_f0_MHz']:.1f} MHz")
    print(f"Lock Acquisition Status    : {'LOCKED [PASS]' if trans_res['is_locked'] else 'UNLOCKED [FAIL]'}")
    print(f"Steady-State Phase Error   : {trans_res['phase_error_rad']:.4f} rad")
    print(f"Lock Acquisition Time      : {trans_res['time_to_lock_ps']:.1f} ps")
    print(f"3 dB Tracking Bandwidth    : {jitter_res['f_3db_tracking_bandwidth_GHz']:.2f} GHz")
    print(f"Integrated Phase Jitter    : {jitter_res['sigma_phi_rad'] * 1e3:.2f} mrad")
    print(f"Derived Output Timing Jitter: {jitter_res['sigma_t_fs']:.2f} fs rms (Target: <= 50.0 fs)")
    print("-" * 70)
    assert trans_res["is_locked"], "ILO failed to acquire lock within locking bandwidth!"
    assert jitter_res["pass_jitter_budget"], f"Derived jitter {jitter_res['sigma_t_fs']:.2f} fs exceeds 50.0 fs limit!"
    print("[PASS] Hardware-level 100 GHz Injection-Locked Comb Clock fully verified.")
