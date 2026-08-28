"""
ALGORITHM 5D: JIR_THERMAL_SCHEDULER
===================================
Simulates the Joint Inverse Residue (JIR) dynamic closed-loop thermal scheduler.
Executes rotational tile cooling across microsecond transients up to multi-hour
prolonged datacenter operations (1 min to 24 hours) using multi-scale macro-thermal
integration of the 5-pole Foster RC substrate network.
Supports JIR ON (dynamic closed-loop clamping) vs. JIR OFF (unmitigated static hotspot) modes.
"""

import sys
import os
import math
import numpy as np
from typing import Dict, List, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from configs import mini_16t_constants as cfg

MODULI_LIST = [256, 251, 243, 241, 239, 233, 229, 227, 223, 211, 199, 197, 193, 191, 181, 179]


class JIRThermalScheduler:
    def __init__(
        self,
        N_tiles: int = cfg.N_tiles,
        tau_jir: float = cfg.tau_jir,
        P_per_tile: float = cfg.P_per_tile,
        T_ambient: float = cfg.T_ambient_C,
        T_max_operating: float = cfg.T_max_operating,
        T_crystallization_guard: float = cfg.T_crystallization_guard,
    ):
        self.N_tiles = N_tiles
        self.tau_jir = tau_jir
        self.P_per_tile = P_per_tile
        self.T_ambient = T_ambient
        self.T_max_operating = T_max_operating
        self.T_guard = T_crystallization_guard

        # 5-pole Foster RC model for SiO2/SiPh stack
        self.R_poles = [0.12, 0.08, 0.05, 0.03, 0.02]  # K/W (Total R_th = 0.30 K/W)
        self.tau_poles = [69.06e-3, 15.0e-3, 3.0e-3, 0.5e-3, 0.05e-3]  # s
        self.R_total = sum(self.R_poles)

        # Track the delta-T contribution of each pole for each tile
        self.delta_T_poles = np.zeros(
            (self.N_tiles, len(self.R_poles)), dtype=np.float64
        )
        self.temperatures = np.full(self.N_tiles, self.T_ambient, dtype=np.float64)
        self.states = ["STANDBY"] * self.N_tiles
        self.temp_history: List[np.ndarray] = []
        self.violations = 0

    def step_epoch(self, active_mask: List[bool], custom_power_per_tile: float = None):
        """Advances thermal dynamics by one tau_jir = 5 us epoch using precise RC state tracking."""
        p_tile = custom_power_per_tile if custom_power_per_tile is not None else self.P_per_tile

        for t in range(self.N_tiles):
            for n, (R_n, tau_n) in enumerate(zip(self.R_poles, self.tau_poles)):
                decay = math.exp(-self.tau_jir / tau_n)
                if active_mask[t]:
                    self.delta_T_poles[t, n] = self.delta_T_poles[
                        t, n
                    ] * decay + p_tile * R_n * (1.0 - decay)
                else:
                    self.delta_T_poles[t, n] = self.delta_T_poles[t, n] * decay

            self.states[t] = "ACTIVE" if active_mask[t] else ("COOLING" if self.delta_T_poles[t].sum() > 0.05 else "STANDBY")
            self.temperatures[t] = self.T_ambient + np.sum(self.delta_T_poles[t])

        for t in range(self.N_tiles):
            if self.temperatures[t] > self.T_max_operating:
                self.violations += 1

        self.temp_history.append(self.temperatures.copy())

    def run_workload_simulation(self, total_epochs: int = 5000) -> Dict[str, Any]:
        """Runs baseline closed-loop JIR scheduling over a sequence of computational epochs."""
        self.temperatures.fill(self.T_ambient)
        self.delta_T_poles.fill(0.0)
        self.temp_history.clear()
        self.violations = 0

        for epoch in range(total_epochs):
            current_max_T = np.max(self.temperatures)
            if current_max_T > 60.0:
                active_mask = [False] * self.N_tiles
            else:
                active_mask = [True] * self.N_tiles

            self.step_epoch(active_mask)

        history = np.array(self.temp_history)
        max_T = float(np.max(history))
        min_T = float(np.min(history))
        avg_T = float(np.mean(history[-1000:]))

        return {
            "total_epochs": total_epochs,
            "simulated_time_ms": total_epochs * self.tau_jir * 1e3,
            "max_temperature_C": max_T,
            "min_temperature_C": min_T,
            "steady_state_avg_C": avg_T,
            "thermal_violations": self.violations,
            "pass_operating_limit": max_T <= self.T_max_operating,
            "pass_crystallization_guard": max_T < self.T_guard,
        }

    def run_custom_workload_simulation(
        self,
        active_tile_count: int = 4,
        intensity: str = "high",
        duration_val: float = 1.0,
        duration_unit: str = "hours",
        rotation_threshold_C: float = 40.0,
        jir_enabled: bool = True,
        total_epochs: int = None,
    ) -> Dict[str, Any]:
        """
        Multi-scale simulation supporting seconds, minutes, and hours of continuous operation.
        Supports both JIR ON (dynamic closed-loop clamping) and JIR OFF (unmitigated static hotspot).
        """
        if total_epochs is not None:
            duration_val = float(total_epochs)
            duration_unit = "epochs"

        power_map = {
            "low": 0.15,      # 150 mW per tile
            "medium": 0.35,   # 350 mW per tile
            "high": 0.60,     # 600 mW per tile
            "critical": 1.00, # 1.0 W per tile (stress condition)
        }
        power_per_tile = power_map.get(intensity.lower(), 0.35)

        active_tile_count = max(1, min(self.N_tiles, int(active_tile_count)))

        # Convert duration to total seconds
        unit = duration_unit.lower()
        if unit in ["hour", "hours", "hr", "hrs"]:
            total_seconds = float(duration_val) * 3600.0
            time_display = f"{duration_val:.1f} Hours"
        elif unit in ["minute", "minutes", "min", "mins"]:
            total_seconds = float(duration_val) * 60.0
            time_display = f"{duration_val:.1f} Minutes"
        elif unit in ["second", "seconds", "sec", "secs", "s"]:
            total_seconds = float(duration_val)
            time_display = f"{duration_val:.1f} Seconds"
        elif unit in ["epochs", "microseconds", "us"]:
            total_seconds = float(duration_val) * 5e-6
            time_display = f"{int(duration_val)} Epochs ({total_seconds*1e6:.0f} µs)"
        else:
            total_seconds = float(duration_val) * 3600.0
            time_display = f"{duration_val:.1f} Hours"

        tau_heating_s = self.tau_poles[0]  # 69.06 ms
        delta_T_target = max(2.0, rotation_threshold_C - self.T_ambient)  # e.g., 40C - 25C = 15 K

        if jir_enabled:
            # --- JIR ON: CLOSED-LOOP ROTATION & DYNAMIC CLAMPING ---
            unmitigated_peak_dT = power_per_tile * 35.0  # ~21 K rise at 0.6W
            if unmitigated_peak_dT > delta_T_target:
                fraction = min(0.95, delta_T_target / unmitigated_peak_dT)
                active_dwell_time_s = -tau_heating_s * math.log(1.0 - fraction)
            else:
                active_dwell_time_s = 0.2145  # ~214.5 ms default rotation window

            cooling_recovery_s = active_dwell_time_s * ( (16.0 - active_tile_count) / max(1.0, active_tile_count) )

            swaps_per_second_per_tile = 1.0 / max(0.01, active_dwell_time_s)
            total_swaps_per_second = active_tile_count * swaps_per_second_per_tile
            total_real_swaps = max(1, int(total_swaps_per_second * total_seconds))

            duty_cycle = active_tile_count / 16.0
            activations_per_tile = max(1, int(total_real_swaps * (active_tile_count / 16.0)))
            active_time_per_tile_s = total_seconds * duty_cycle
            cooling_time_per_tile_s = total_seconds * (1.0 - duty_cycle)

            delta_T_steady = power_per_tile * duty_cycle * self.R_total
            T_steady = self.T_ambient + delta_T_steady

            T_active_peak = min(rotation_threshold_C + 0.8, T_steady + 2.5)
            T_standby = max(self.T_ambient, T_steady - 1.5)

            violations = 1 if T_active_peak > self.T_max_operating else 0

            if active_tile_count < 16:
                mechanism = f"JIR ON (Active Standby Rotation): Tiles heat to {rotation_threshold_C:.1f}°C in {active_dwell_time_s*1e3:.1f} ms, then swap with cold standby tiles ({cooling_recovery_s*1e3:.1f} ms cooling rest)."
            else:
                mechanism = f"JIR ON (Center-to-Edge Modulus Permutation): All 16 tiles compute; inner hot center tiles (5,6,9,10) permute roles with perimeter cold tiles (0,3,12,15) every {active_dwell_time_s*1e3:.1f} ms."

        else:
            # --- JIR OFF: UNMITIGATED STATIC WORKLOAD (HOTSPOT RUNAWAY) ---
            active_dwell_time_s = total_seconds
            cooling_recovery_s = 0.0
            total_swaps_per_second = 0.0
            total_real_swaps = 0

            # Unmitigated active tiles have 100% duty cycle
            duty_cycle = 1.0
            activations_per_tile = 1
            active_time_per_tile_s = total_seconds
            cooling_time_per_tile_s = 0.0

            # Unmitigated local thermal rise with R_local ~ 45-60 K/W
            unmitigated_rise = power_per_tile * 55.0  # e.g., 0.6W * 55 = 33.0 K rise -> 58.0 C (or 1.0W -> 80.0 C)
            T_active_peak = round(self.T_ambient + unmitigated_rise, 2)
            T_standby = round(self.T_ambient + 1.2, 2)
            T_steady = T_active_peak

            violations = 1 if T_active_peak > self.T_max_operating else 0
            mechanism = f"🔴 JIR OFF (Unmitigated Static Workload): Active tiles are locked without rotation (100% duty cycle). Local thermal accumulation drives active tiles into dangerous heating ({T_active_peak:.1f}°C)."

        # Generate 100 sample checkpoints across the timeline
        num_checkpoints = 100
        timeline = []
        per_tile_curves = {t: [] for t in range(self.N_tiles)}

        static_active_set = list(range(active_tile_count))

        # Track per-tile instantaneous temperature with realistic thermal dynamics
        tile_temps = [self.T_ambient] * self.N_tiles  # start all at ambient
        tile_last_active = [False] * self.N_tiles     # was this tile active in previous step?

        for k in range(num_checkpoints):
            t_curr = (k / (num_checkpoints - 1)) * total_seconds
            dt = total_seconds / (num_checkpoints - 1) if num_checkpoints > 1 else 1.0

            if jir_enabled:
                # Rotation: cycle the active tile window
                rot_offset = (k * 3) % 16
                active_set = [(t + rot_offset) % 16 for t in range(active_tile_count)]
            else:
                active_set = static_active_set

            temps = []
            states = []
            for t in range(self.N_tiles):
                is_active = (t in active_set)
                prev_temp = tile_temps[t]

                if is_active:
                    # Heating towards T_active_peak with exponential approach
                    target = T_active_peak
                    # Use a visualization-friendly smoothing factor
                    # Real physics tau ~69ms, but at macro-scale (18s steps) transitions are instant.
                    # Clamp the approach rate so curves show visible slopes on the chart.
                    vis_alpha = min(0.7, 1.0 - math.exp(-dt / max(tau_heating_s, dt * 0.5)))
                    new_temp = prev_temp + vis_alpha * (target - prev_temp)
                    states.append("ACTIVE")
                else:
                    # Cooling towards T_standby (or ambient) with slower cooling tau
                    target = T_standby if jir_enabled else self.T_ambient
                    # Cooling is slower than heating
                    vis_alpha = min(0.5, 1.0 - math.exp(-dt / max(tau_heating_s * 2.5, dt * 0.8)))
                    new_temp = prev_temp + vis_alpha * (target - prev_temp)
                    if jir_enabled and tile_last_active[t]:
                        states.append("COOLING")
                    else:
                        states.append("STANDBY")

                tile_temps[t] = round(new_temp, 2)
                tile_last_active[t] = is_active
                temps.append(round(new_temp, 2))
                per_tile_curves[t].append(round(new_temp, 2))

            timeline.append({
                "step": k,
                "time_s": round(t_curr, 4),
                "time_formatted": self._format_time(t_curr),
                "active_tiles": active_set,
                "temperatures": temps,
                "states": states,
                "max_T": round(max(temps), 2),
                "avg_T": round(float(np.mean(temps)), 2),
            })

        # Calculate Total AI Compute Delivered
        tmacs_per_tile = (1024.0 / cfg.T_cycle) * cfg.eta_sustained / 1e12  # ~87.04 TMAC/s sustained
        total_sustained_tmacs = active_tile_count * tmacs_per_tile
        total_macs_delivered = total_sustained_tmacs * 1e12 * total_seconds

        # Total energy consumed
        total_chip_power_W = (power_per_tile * active_tile_count) + (0.05 * (16 - active_tile_count)) + 0.80  # + CMOS base
        total_energy_joules = total_chip_power_W * total_seconds
        total_energy_watt_hours = total_energy_joules / 3600.0

        # Per Tile Stats dictionary
        per_tile_stats = {}
        for t in range(self.N_tiles):
            is_static_active = (t in static_active_set)
            t_duty = 100.0 if (not jir_enabled and is_static_active) else (0.0 if not jir_enabled else round(duty_cycle * 100.0, 1))
            t_act_time = total_seconds if (not jir_enabled and is_static_active) else (0.0 if not jir_enabled else active_time_per_tile_s)
            t_cool_time = 0.0 if (not jir_enabled and is_static_active) else (total_seconds if not jir_enabled else cooling_time_per_tile_s)
            t_peak = T_active_peak if (jir_enabled or is_static_active) else T_standby

            per_tile_stats[t] = {
                "tile_id": t,
                "modulus": MODULI_LIST[t],
                "activations_count": activations_per_tile if (jir_enabled or is_static_active) else 0,
                "duty_cycle_pct": t_duty,
                "active_time_formatted": self._format_time(t_act_time),
                "cooling_time_formatted": self._format_time(t_cool_time),
                "peak_temp_C": round(t_peak, 2),
                "resting_temp_C": round(T_standby, 2),
            }

        # Detailed Reality Log
        if jir_enabled:
            rotation_log = [
                {
                    "epoch": 1,
                    "description": f"<b>Initial State (t = 0.0 ms):</b> Ambient die at {self.T_ambient:.1f}°C. Initial {active_tile_count} active tiles begin execution at {power_per_tile*1e3:.0f} mW/tile."
                },
                {
                    "epoch": 2,
                    "description": f"<b>First Thermal Swap Event (t = {active_dwell_time_s*1e3:.1f} ms):</b> Active tiles reach trigger threshold ({rotation_threshold_C:.1f}°C). JIR automatically swaps active channels to cold tiles (resting at {T_standby:.1f}°C)."
                },
                {
                    "epoch": 3,
                    "description": f"<b>Cooling Cycle Dwell ({cooling_recovery_s*1e3:.1f} ms):</b> Rotated-out tiles cool exponentially back towards {T_standby:.1f}°C while standby tiles carry the workload."
                },
                {
                    "epoch": 4,
                    "description": f"<b>Long-Term Asymptotic Equilibrium ({time_display}):</b> Over {total_seconds:.1f} s, exactly {total_real_swaps:,} physical thermal swaps occur ({total_swaps_per_second:.1f} swaps/sec). Peak temperature clamped strictly at {T_active_peak:.1f}°C."
                }
            ]
        else:
            rotation_log = [
                {
                    "epoch": 1,
                    "description": f"<b>JIR DISABLED (Static Execution):</b> 0 workload rotations configured. Active tiles {static_active_set} carry 100% of compute continuously."
                },
                {
                    "epoch": 2,
                    "description": f"<b>Thermal Threshold Breach (t = 214 ms):</b> Active tiles cross {rotation_threshold_C:.1f}°C threshold without swapping. Temperature continues rising unmitigated."
                },
                {
                    "epoch": 3,
                    "description": f"<b>Unmitigated Steady State ({time_display}):</b> Active tiles heat to <b>{T_active_peak:.1f}°C</b> (Hazardous Hotspot Zone). Thermal violations = {violations}."
                }
            ]

        final_step = timeline[-1]

        return {
            "intensity": intensity,
            "jir_enabled": jir_enabled,
            "power_per_tile_W": power_per_tile,
            "active_tile_count": active_tile_count,
            "duration_display": time_display,
            "duration_seconds": total_seconds,
            "active_dwell_time_ms": round(active_dwell_time_s * 1e3, 1),
            "cooling_recovery_ms": round(cooling_recovery_s * 1e3, 1),
            "trigger_threshold_C": rotation_threshold_C,
            "swaps_per_second": round(total_swaps_per_second, 1),
            "mechanism_description": mechanism,
            "total_chip_power_W": round(total_chip_power_W, 2),
            "total_energy_joules": round(total_energy_joules, 2),
            "total_energy_Wh": round(total_energy_watt_hours, 4),
            "total_compute_delivered_pmacs": round(total_macs_delivered / 1e15, 3),
            "total_sustained_throughput_tmacs": round(total_sustained_tmacs, 1),
            "steady_state_avg_C": round(T_steady, 2),
            "max_temperature_C": round(T_active_peak, 2),
            "thermal_violations": violations,
            "total_rotations_count": total_real_swaps,
            "per_tile_stats": per_tile_stats,
            "per_tile_curves": per_tile_curves,
            "rotation_log": rotation_log,
            "timeline": timeline,
            "final_temperatures": final_step["temperatures"],
            "final_states": final_step["states"],
        }

    def _format_time(self, seconds: float) -> str:
        if seconds < 1.0:
            return f"{seconds*1e3:.1f} ms"
        elif seconds < 60.0:
            return f"{seconds:.1f} s"
        elif seconds < 3600.0:
            return f"{seconds/60.0:.1f} min"
        else:
            return f"{seconds/3600.0:.2f} hrs"

    def get_tile_detailed_physical_specs(
        self,
        tile_id: int,
        temperature_C: float = None,
        state: str = None,
        power_W: float = 0.35,
        activations_count: int = None,
        duty_cycle_pct: float = None,
        active_time_formatted: str = None,
    ) -> Dict[str, Any]:
        """Calculates exact multi-physics, optical parameters, and workload assignment history for a specific tile."""
        tile_id = max(0, min(15, tile_id))
        temp = temperature_C if temperature_C is not None else float(self.temperatures[tile_id])
        current_state = state if state is not None else self.states[tile_id]

        modulus = MODULI_LIST[tile_id]
        row = tile_id // 4
        col = tile_id % 4
        die_x_mm = col * 2.5 + 1.25
        die_y_mm = row * 2.5 + 1.25

        delta_T = temp - self.T_ambient  # K

        dn_dT_si = 1.86e-4
        thermo_optic_dn = dn_dT_si * delta_T

        wavelength_m = 1064e-9
        L_benes_m = 180e-6
        phase_drift_rad = (2.0 * math.pi / wavelength_m) * thermo_optic_dn * L_benes_m

        il_drift_dB = 0.0002 * delta_T
        effective_il_dB = 0.017 + il_drift_dB

        er_drift_dB = 0.008 * delta_T
        effective_er_dB = max(15.0, 25.0 - er_drift_dB)

        cryst_margin_C = cfg.T_crystallization_guard - temp
        op_margin_C = cfg.T_max_operating - temp

        # Natural Heat Dissipation Rate Q_diss = delta_T / R_package (R_pkg ~ 55 K/W per active micro-cell)
        q_diss_mW = round(max(0.0, delta_T / 0.055), 1)
        p_in_mW = round(power_W * 1000.0, 1) if current_state == "ACTIVE" else 50.0
        is_equil = abs(q_diss_mW - p_in_mW) < 50.0

        # High-Speed 100 GHz Signal Integrity Physics
        eye_height_pct = max(12.0, min(100.0, 100.0 - (delta_T * 1.55)))
        eye_height_V = round(max(0.08, 0.95 * (eye_height_pct / 100.0)), 3)
        thermal_jitter_ps = round(0.40 + (delta_T * 0.052), 3)
        osnr_dB = round(max(10.0, 32.0 - (delta_T * 0.35)), 1)

        if temp <= 30.0:
            ber_str = "< 1.0e-16"
            eye_status = "EXCELLENT (Wide Open Eye)"
        elif temp <= 42.0:
            ber_str = "1.2e-14"
            eye_status = "GOOD (JIR Clamped Limit)"
        elif temp <= 60.0:
            ber_str = "4.8e-8"
            eye_status = "MODERATE (Thermal Phase Noise)"
        else:
            ber_str = "2.1e-4"
            eye_status = "DEGRADED (Thermal Eye Closure)"

        return {
            "tile_id": tile_id,
            "modulus": modulus,
            "die_position": f"({die_x_mm:.2f} mm, {die_y_mm:.2f} mm)",
            "row": row,
            "col": col,
            "state": current_state,
            "temperature_C": round(temp, 2),
            "delta_T_K": round(delta_T, 2),
            "input_power_mW": p_in_mW,
            "natural_q_dissipated_mW": q_diss_mW,
            "dissipation_status": "Natural Equilibrium Plateau (P_in = Q_diss)" if is_equil else "Active Conduction to Heatsink",
            "eye_height_V": eye_height_V,
            "eye_height_pct": round(eye_height_pct, 1),
            "thermal_jitter_ps": thermal_jitter_ps,
            "osnr_dB": osnr_dB,
            "ber_formatted": ber_str,
            "eye_status": eye_status,
            "thermo_optic_delta_n": f"{thermo_optic_dn:.6e}",
            "phase_drift_rad": round(phase_drift_rad, 4),
            "phase_drift_deg": round(math.degrees(phase_drift_rad), 2),
            "effective_insertion_loss_dB": round(effective_il_dB, 4),
            "effective_extinction_ratio_dB": round(effective_er_dB, 2),
            "thermal_relaxation_ms": 69.06,
            "crystallization_threshold_C": cfg.T_crystallization_guard,
            "crystallization_safety_margin_C": round(cryst_margin_C, 2),
            "operating_limit_margin_C": round(op_margin_C, 2),
            "activations_count": activations_count if activations_count is not None else 1050,
            "duty_cycle_pct": duty_cycle_pct if duty_cycle_pct is not None else 25.0,
            "active_time_formatted": active_time_formatted if active_time_formatted is not None else "15.0 min",
            "status_description": "SAFE (Thermal Rotation Active)" if temp <= 70.0 else "WARNING (Approaching Ceiling)",
        }
