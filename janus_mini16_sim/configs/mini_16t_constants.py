"""
PROJECT JANUS MINI (16-TILE): GLOBAL SIMULATION CONSTANTS REGISTRY
==================================================================
Document ID: JANUS-SIM-SPEC-MINI16-2026-V1
Target Hardware: JANUS Mini 16-Tile Monolithic Planar MVP (Model 1A)

This module defines all immutable simulation constants shared across
all verification tiers (Tier 0 to Tier 5).
"""

import json
import math
import os
from typing import Dict

# ==============================================================================
# 2.0 TIER 0: GDS II LAYOUT PRE-PROCESSOR & PHYSICAL GEOMETRY
# ==============================================================================
GDS_FILE_PATH: str = r"c:\Users\hp\Desktop\Janus Update\janus_mini16_layout.gds"
LAYER_MAP: Dict[str, str] = {
    "1": "Si_Waveguide",
    "2": "SiO2_Cladding",
    "3": "Sb2S3_Patch",
    "4": "LiTaO3_Modulator",
    "5": "Germanium_APD",
    "6": "Metal_TDV_Copper",
}
POLYGON_TOLERANCE: float = 1e-9  # 1 nm tolerance for polygon simplification (m)

# ==============================================================================
# 2.1 UNIVERSAL PHYSICAL CONSTANTS
# ==============================================================================
c_vacuum: float = 2.9979e8  # Speed of light in vacuum (m/s) [T1, T3]
h_planck: float = 6.626e-34  # Planck's constant (J-s) [T1, T3]
h_bar: float = 1.0546e-34  # Reduced Planck's constant (h/2pi) (J-s) [T1]
k_boltzmann: float = 1.381e-23  # Boltzmann constant (J/K) [T3]
q_electron: float = 1.602e-19  # Elementary charge (C) [T3]
epsilon_0: float = 8.854e-12  # Permittivity of free space (F/m) [T1, T3]
mu_0: float = 1.2566e-6  # Permeability of free space (H/m) [T1]
pi: float = math.pi  # Mathematical constant pi (dimensionless) [All]

# ==============================================================================
# 2.2 OPERATING WAVELENGTH, LASER SOURCE & OPTICAL CARRIER
# ==============================================================================
lambda_0: float = 1064e-9  # Primary operating wavelength (m) [T1, T3]
lambda_0_nm: float = 1064.0  # Operating wavelength (nm) [T1]
f_optical: float = 281.76e12  # Optical carrier frequency (Hz) [T1, T3]
omega_optical: float = 1.7703e15  # Angular optical frequency (rad/s) [T1]
E_photon: float = 1.8669e-19  # Single photon energy (J) [T1, T3]
E_photon_eV: float = 1.1654  # Photon energy in electron-volts (eV) [T1, T3]
lambda_pump: float = 976e-9  # Yb-fiber pump wavelength (m) [T1]
eta_qd_yb: float = 0.917  # Yb quantum defect efficiency (976/1064) [T1]
N_lambda: int = 1  # Number of wavelength channels (single-lambda) [T1]
P_ghost: float = 0.0  # Parasitic FWM ghost power (W) [T1]

# ==============================================================================
# 2.3 OPTICAL MATERIAL REFRACTIVE INDICES & ELECTRO-OPTIC COEFFICIENTS
# ==============================================================================
n_si: float = 3.565  # Silicon refractive index at 1064 nm [T1]
n_sio2: float = 1.444  # SiO2 cladding refractive index at 1064 nm [T1]
n_sin: float = 2.01  # Si3N4 waveguide refractive index at 1064 nm [T1]
n_litao3: float = 2.13  # LiTaO3 refractive index at 1064 nm [T1]
n_sb2s3_amorph: float = 2.7  # Sb2S3 amorphous index at 1064 nm [Ref: Dong et al., 2022]
k_sb2s3_amorph_base: float = (
    0.0001  # Base amorphous extinction coefficient at 300K [Ref: Dong et al., 2022]
)
n_sb2s3_cryst: float = (
    3.3  # Sb2S3 crystalline real refractive index at 1064 nm [Ref: Dong et al., 2022] [T1]
)
k_sb2s3_cryst_base: float = (
    0.001  # Base crystalline extinction coefficient at 300K [Ref: Dong et al., 2022]
)


def get_k_sb2s3(state: str, temperature_K: float = 300.0) -> float:
    k_base = k_sb2s3_cryst_base if state == "crystalline" else k_sb2s3_amorph_base
    return k_base * (1.0 + 0.005 * max(0.0, temperature_K - 300.0))


n_real_cu: float = 0.28  # Metal 1 Copper real refractive index
n_imag_cu: float = 11.0  # Metal 1 Copper extinction coefficient
n_real_sac2m: float = 4.27  # SAC2M Ge/Si APD real refractive index
n_imag_sac2m: float = 0.08  # SAC2M Ge/Si APD extinction coefficient
delta_n_pcm: float = 0.75  # PCM refractive index contrast (n_c - n_a) [T1]
delta_n_pcm_range_max: float = 2.5  # Maximum observed PCM delta_n [T1]
dn_dT_si: float = 1.86e-4  # Thermo-optic coefficient of silicon (1/K) [T1, T2]
r33_litao3: float = 30.5e-12  # LiTaO3 Pockels electro-optic coefficient (m/V) [T1]
loss_sin_prop: float = 0.1  # Si3N4 waveguide propagation loss (dB/cm) [T1]
loss_litao3_prop: float = 0.1  # LiTaO3 waveguide propagation loss (dB/cm) [T1]

# ==============================================================================
# 2.4 PHASE-CHANGE MATERIAL (Sb2S3) PROPERTIES
# ==============================================================================
T_crystallization_min: float = (
    200.0  # Sb2S3 SET min crystallization temp (deg-C) [T1, T2]
)
T_crystallization_max: float = (
    220.0  # Sb2S3 SET max crystallization temp (deg-C) [T1, T2]
)
T_melting_min: float = 500.0  # Sb2S3 RESET min melting temp (deg-C) [T1, T2]
T_melting_max: float = 540.0  # Sb2S3 RESET max melting temp (deg-C) [T1, T2]
E_pcm_program_min: float = 10e-12  # PCM programming energy min (J) [T1, T3]
E_pcm_program_max: float = 50e-12  # PCM programming energy max (J) [T1, T3]
cycling_endurance: float = 1e6  # Sb2S3 switch cycling endurance floor (cycles) [T1]
cycling_endurance_max: float = 1e8  # Sb2S3 demonstrated endurance ceiling (cycles) [T1]
volumetric_expansion_min: float = 4.0  # Volumetric strain min (%) [T1, T2]
volumetric_expansion_max: float = 8.0  # Volumetric strain max (%) [T1, T2]
k_gst_thermal: float = 0.5  # Sb2S3 thermal conductivity (W/(m-K)) [T2]
A_pcm_cell: float = 1.25e-12  # Single PCM switch footprint (1.25 um^2) (m^2) [T1, T2]
V_gap_pcm: float = 25e-9  # Nanoscale engineered void gap (m) [T1, T2]
V_gap_minimum: float = 20e-9  # Absolute minimum void gap (m) [T1, T2]
gst_patch_thickness: float = 15e-9  # Sb2S3 active patch thickness (m) [T1]
P_pcm_static_hold: float = 0.0  # Non-volatile PCM static hold power (W) [T3, T5]

# ==============================================================================
# 2.5 WAVEGUIDE & PHOTONIC CELL GEOMETRY
# ==============================================================================
wg_width_si: float = 450e-9  # Silicon waveguide core width (m) [T1]
wg_height_si: float = 220e-9  # Silicon waveguide core height (m) [T1]
L_wg_phase: float = 500e-6  # Waveguide length for phase stability (m) [T1, T2]
L_wire_electrical: float = 200e-6  # On-chip local electrical wire length (m) [T3, T4]
v_wire: float = 1.5e8  # Speed of light in on-chip metal (c/2) (m/s) [T3, T4]
IL_crossing: float = 0.02  # MMI waveguide crossing insertion loss (dB) [T1]
XT_crossing: float = -40.0  # MMI waveguide crossing crosstalk (dB) [T1]

mmi_W_um: float = 1.6  # MMI width (um)
mmi_L_um: float = 6.4  # MMI length (um)
mmi_s11_mag_db: float = -46.0  # MMI S11 magnitude (dB)
mmi_phase_s11: float = 0.05  # MMI S11 phase (rad)
mmi_phase_s21: float = 0.0  # MMI S21 phase (rad)
mmi_phase_s31: float = 1.57  # MMI S31 phase (rad)
mmi_phase_s41: float = -1.57  # MMI S41 phase (rad)

gst_iso_11_am: float = -42.0
gst_iso_11_cr: float = -40.0
gst_iso_41: float = -45.0
gst_phase_am: float = 0.02
gst_phase_11: float = 0.1
gst_phase_41: float = 0.5

gap_eo_nm: float = 300.0  # LiTaO3 Pockels gap (nm)
L_active_um: float = 500.0  # LiTaO3 active length (um)
R_eff: float = 25.0  # Effective resistance (Ohm)
C_junction: float = 63.66e-15  # Junction capacitance (F)

# ==============================================================================
# 2.6 MINI 16-TILE ARCHITECTURAL TOPOLOGY
# ==============================================================================
N_tiles: int = 16  # Number of independent residue tiles [All]
N_dim: int = 32  # Matrix dimension per tile (32 x 32 mesh) [All]
N_mult_per_tile: int = 1024  # Multipliers per tile (N_dim^2 = 32^2) [All]
N_mult_total: int = 16384  # Total optical multipliers (N_tiles * N_mult_per_tile) [All]
N_alphabet: int = 256  # Waveguide alphabet per multiplier (1-Hot 8-bit) [T1, T5]
N_alphabet_bits: int = 8  # Bit-width of spatial alphabet (log2(256)) [T4, T5]
N_wg_total: int = 4194304  # Total spatial waveguides (N_mult_total * N_alphabet) [T1]
S_benes: int = 15  # Benes switching stages (2*log2(256) - 1) [T1, T5]
N_switch_per_mult: int = 1920  # Switches per multiplier fabric ((N/2) * S) [T1, T5]
N_switch_total: int = 31457280  # Total Sb2S3 switch cells (~31.46 M) [T1, T2]
N_apd_total: int = 4194304  # Total SAC2M Ge/Si APD detectors (~4.19 M) [T3]
N_active_per_cycle: int = 16384  # Active photons per 10 ps cycle [T1, T3, T5]
N_active_per_phase: int = 8192  # Active photons per 5 ps half-cycle phase [T1, T3]
alpha_spatial: float = 1.0 / 256.0  # Spatial activity factor (1-in-N sparsity) [T3, T5]
alpha_spatial_decimal: float = 0.00390625  # Decimal spatial activity factor [T3, T5]

# ==============================================================================
# 2.7 DIE GEOMETRY & Z-AXIS PHYSICAL STACK
# ==============================================================================
A_die: float = 100.00e-6  # Die footprint area (m^2) [T2]
A_die_mm2: float = 100.00  # Die footprint area (mm^2) [T2]
L_die: float = 10.0e-3  # Die side length (m) [T2]
A_tile: float = 6.25e-6  # Individual tile area (m^2) [T2]
A_apd_single: float = 1.5e-12  # Single Ge/Si APD device area (m^2) [T1, T3]
h_cmos: float = 50e-6  # CMOS base substrate thickness (m) [T2]
h_sio2_buffer: float = 250e-6  # SiO2 monolithic thermal buffer thickness (m) [T2]
h_siph: float = 30e-6  # SiPh stratum thickness (m) [T2]
N_strata: int = 1  # SiPh strata count (Gen-1 planar monolithic) [T2]
h_total_active: float = 330e-6  # Total active die height (50+250+30 um) (m) [T2]
h_inter_stratum_sio2: float = 0.0  # Inter-stratum SiO2 spacer (m) [T2]

# ==============================================================================
# 2.8 HEAT SPREADER & PACKAGE DIMENSIONS
# ==============================================================================
h_hs1: float = 30e-6  # Heat Spreader 1 thickness (m) [T2]
h_spreader_gap: float = 50e-6  # Spreader gap thickness (m) [T2]
h_hs2: float = 250e-6  # Heat Spreader 2 thickness (m) [T2]
h_package_added: float = 330e-6  # Total package added height (m) [T2]
h_package_total: float = 660e-6  # Total packaged system height (m) [T2]
rho_cu_pillar_sparse: float = 10000.0  # Sparse Cu-pillar density (mm^-2) [T2]
rho_cu_pillar_dense: float = 900000.0  # Dense Cu-pillar density (mm^-2) [T2]
rho_cu_pillar_hs: float = 950000.0  # HS1 to HS2 Cu-pillar density (mm^-2) [T2]
h_hbm_reference: float = 720e-6  # Reference HBM stack height (m) [T2]

# ==============================================================================
# 2.9 - 2.14 THERMAL MATERIAL PROPERTIES
# ==============================================================================
k_si_thermal: float = 148.0  # Thermal conductivity (W/(m-K)) [T2]
rho_si: float = 2330.0  # Mass density (kg/m^3) [T2]
cp_si: float = 705.0  # Specific heat capacity (J/(kg-K)) [T2]
alpha_si_thermal: float = 9.010e-5  # Thermal diffusivity (m^2/s) [T2]

k_sio2_thermal: float = 1.38  # Thermal conductivity (W/(m-K)) [T2]
rho_sio2: float = 2200.0  # Mass density (kg/m^3) [T2]
cp_sio2: float = 703.0  # Specific heat capacity (J/(kg-K)) [T2]
alpha_sio2: float = 9.05e-7  # Thermal diffusivity (m^2/s) [T2]
m_sio2_buffer: float = 5.500e-5  # SiO2 buffer mass (kg) [T2]
C_sio2_buffer: float = 38.66e-3  # SiO2 buffer heat capacity (J/K) [T2]

k_cu: float = 400.0  # Thermal conductivity (W/(m-K)) [T2]
rho_cu: float = 8960.0  # Mass density (kg/m^3) [T2]
cp_cu: float = 385.0  # Specific heat capacity (J/(kg-K)) [T2]
alpha_cu: float = 1.160e-4  # Thermal diffusivity (m^2/s) [T2]

k_ge: float = 60.0  # Thermal conductivity (W/(m-K)) [T2]
rho_ge: float = 5323.0  # Mass density (kg/m^3) [T2]
cp_ge: float = 320.0  # Specific heat capacity (J/(kg-K)) [T2]
alpha_ge: float = 3.52e-5  # Thermal diffusivity (m^2/s) [T2]

k_air: float = 0.026  # Thermal conductivity (W/(m-K)) [T2]

k_litao3: float = 4.6  # Thermal conductivity (W/(m-K)) [T2]
rho_litao3: float = 7456.0  # Mass density (kg/m^3) [T2]
cp_litao3: float = 424.0  # Specific heat capacity (J/(kg-K)) [T2]

# ==============================================================================
# 2.15 THERMAL DYNAMICS & JIR SCHEDULING
# ==============================================================================
T_ambient: float = 298.15  # Ambient reference temperature (K) [T2]
T_ambient_C: float = 25.0  # Ambient reference temperature (deg-C) [T2]
tau_diff: float = 69.06e-3  # SiO2 thermal diffusion time (s) [T2, T5]
tau_diff_ms: float = 69.06  # Thermal diffusion time (ms) [T2, T5]
tau_jir: float = 5.0e-6  # JIR activation cycle duration (s) [T2, T5]
tau_jir_us: float = 5.0  # JIR activation cycle (us) [T2, T5]
N_jir_per_tau_diff: int = 13812  # JIR cycles per thermal diffusion time [T2, T5]
t_jir_rotation: float = 4.0e-6  # JIR state-transition overhead (s) [T5]
Q_gen_per_jir: float = 30.85e-6  # Heat generated per JIR cycle (J) [T2, T5]
delta_T_cycle: float = 0.798e-3  # Per-cycle thermal transient rise (K) [T2, T5]
delta_T_cycle_mK: float = 0.798  # Per-cycle thermal rise (mK) [T2, T5]
delta_T_crit_phase: float = 5.72  # Phase-drift critical temperature rise (K) [T1, T2]
delta_T_steady: float = 0.213  # Steady-state SiPh temp rise (K) [T2]
thermal_margin_ratio: float = 26.9  # Thermal stability margin (dT_crit/dT_ss) [T2]
T_max_operating: float = 70.0  # Nominal commercial operating ceiling (deg-C) [T2, T5]
T_max_operating_K: float = 343.15  # Nominal commercial operating ceiling (K) [T2, T5]
T_retention_max: float = (
    100.0  # Hard physical 10-year Sb2S3 retention limit (deg-C) [T2, T5]
)
T_crystallization_guard: float = 150.0  # GST crystallization onset temp (deg-C) [T2]
R_th_down: float = 0.195  # Downward CMOS-SiO2 thermal resistance (K/W) [T2]
R_th_up: float = 0.552  # Upward SiPh-HS1 thermal resistance (K/W) [T2]
P_per_tile: float = 0.386  # Average power dissipation per tile (W) [T2, T5]
delta_T_permissible_siph: float = (
    0.048  # Permissible SiPh stability window (K) [T1, T2]
)

# ==============================================================================
# 2.16 - 2.18 APD & RECEIVER ELECTRONICS
# ==============================================================================
M_apd: int = 7  # APD avalanche multiplication gain [T3]
k_ionization: float = 0.06  # Effective impact ionization ratio [T3]
F_excess_noise: float = 2.0  # McIntyre excess noise factor [T3]
R_responsivity: float = 0.8  # Germanium responsivity at 1064 nm (A/W) [T3]
f_3db_apd: float = 105e9  # APD 3 dB electrical bandwidth (Hz) [T3]
GBP_apd: float = 441e9  # Gain-bandwidth product (Hz) [T3]
t_pd_clearance: float = 1.52e-12  # Photogenerated carrier clearance time (s) [T3]
C_j_apd: float = 0.8e-15  # APD junction capacitance (F) [T3]
R_s_apd: float = 25.0  # APD series resistance (ohm) [T3]
C_int_parasitic: float = 3.0e-15  # Maximum parasitic input capacitance (F) [T3]
I_dark_apd: float = 1e-9  # APD dark current upper bound (A) [T3]
I_surface_leakage: float = 0.5e-9  # Unmultiplied surface leakage dark current (A) [T3]
I_bulk_dark: float = (
    0.05e-9  # Bulk dark current before avalanche multiplication (A) [T3]
)

sigma_latch_noise: float = (
    0.5e-6  # Input-referred RMS noise of StrongARM latch (A) [T3]
)
E_strongarm: float = 100e-18  # StrongARM per-decision energy (J) [T3, T4]
t_regen: float = 3.5e-12  # StrongARM regeneration time (s) [T3, T4]
E_pockels_switch: float = 50e-18  # Pockels EO switch energy (J) [T1, T3]

C_p_strongarm: float = 5.0e-15  # StrongARM sensing-node parasitic capacitance [T3]
t_int_strongarm: float = (
    5.0e-12  # Charge integration window before regeneration (s) [T3]
)
g_m_latch: float = (
    8.0e-3  # StrongARM cross-coupled pair effective transconductance (S) [T3]
)
t_setup: float = 1.0e-12  # Latch setup/decision timing guard (s) [T3]
jitter_rms: float = 50e-15  # Pulse timing jitter, comb-referenced clock (s) [T6]

BER_target: float = 1e-18  # Target bit error rate [T3, T5]
Q_factor: float = 9.38  # Q-factor for BER=10^-18 [T3]
P_sens_theoretical: float = 3.01e-6  # Theoretical receiver sensitivity (W) [T3]
P_sens_theoretical_dbm: float = -25.21  # Theoretical sensitivity (dBm) [T3]
sensitivity_margin_db: float = 2.0  # Engineering margin (dB) [T3]
P_sens_practical: float = 4.79e-6  # Practical receiver sensitivity (W) [T3]
P_sens_practical_dbm: float = -23.21  # Practical sensitivity (dBm) [T3]
P_det: float = 13.82e-6  # Delivered signal power at detector (W) [T3]
P_det_dbm: float = -18.59  # Delivered power in dBm [T3]
link_margin: float = 4.61  # Net binary detection margin (dB) [T3]
link_margin_linear: float = 2.89  # Linear power safety factor [T3]
P_false_positive: float = 2.55e-16  # Dark-channel false positive probability [T3, T5]

# ==============================================================================
# 2.19 - 2.21 POWER & LOSS BUDGETS
# ==============================================================================
P_laser_optical: float = 2.21  # Master laser CW optical power (W) [T1, T3]
P_laser_optical_dbm: float = 33.44  # Laser optical power in dBm [T1, T3]
WPE: float = 0.75  # Laser wall-plug efficiency [T3]
P_laser_electrical: float = 2.95  # Laser electrical consumption (W) [T3]

N_mmi_stages: int = 13  # Cascaded 1:2 MMI splitter count [T1]
L_split_per_stage: float = 3.0103  # Ideal per-stage splitting loss (dB) [T1]
L_split_ideal: float = 39.13  # Total ideal splitting loss (dB) [T1]
L_mmi_excess_per_stage: float = 0.30  # MMI excess loss per stage (dB) [T1]
L_mmi_excess_total: float = 3.90  # Total MMI excess loss (dB) [T1]
L_benes_per_stage: float = 0.50  # Dilated Benes loss per stage (dB) [T1]
L_benes_total: float = 7.50  # Total 15-stage Benes loss (dB) [T1]
L_propagation_coupling: float = 1.50  # Propagation & interlayer loss (dB) [T1]
L_excess_total: float = 12.90  # Total excess path loss (dB) [T1]
L_distribution_total: float = 52.03  # Total distribution loss (dB) [T1, T3]
IL_switch_cell: float = 0.10  # Sb2S3 switch insertion loss (dB) [T1]
ER_dilated_benes: float = 25.0  # Dilated Benes extinction ratio (dB) [T1]

P_litao3_routers: float = 0.51  # LiTaO3 router power (W) [T3]
P_apd_detectors: float = 0.16  # Ge/Si APD array power (W) [T3]
P_optical_amp: float = 0.0  # Optical amp power (eliminated = 0 W) [T3]
P_cmos_logic: float = 1.05  # CMOS encoders/adders/CRT power (W) [T3, T4]
P_jir_control: float = 1.50  # JIR scheduler and control power (W) [T4, T5]
P_total_system: float = 6.17  # Total full-system power (W) [All]

# ==============================================================================
# 2.22 TIMING, FREQUENCY & LATENCY BUDGET
# ==============================================================================
f_clk: float = 100e9  # System operating clock frequency (100 GHz) [All]
T_cycle: float = 10.0e-12  # Clock cycle period (10.0 ps) [All]
T_phase: float = 5.0e-12  # Illumination phase duration (5.0 ps) [T1, T3]
tau_fwhm_min: float = 3.0e-12  # Minimum optical pulse FWHM (s) [T1]
tau_fwhm_max: float = 5.0e-12  # Maximum optical pulse FWHM (s) [T1]
t_mod: float = 10.0e-12  # EO injection pulse interval (s) [T1, T3]
t_wire: float = 1.33e-12  # Local electrical interconnect delay (s) [T3, T4]
t_guard: float = 3.5e-12  # Inter-pulse guard margin (s) [T1, T3]
t_opt_benes: float = 750e-12  # 15-stage Benes propagation delay (s) [T1]
t_crt: float = 80e-12  # CRT adder-tree delay (80 ps = 8 stages @ 10 ps) [T4]
N_crt_pipeline_stages: int = 8  # CRT pipelined adder tree stages [T4]
T_latency_total: float = 963e-12  # Total end-to-end latency (963 ps) [T1-T4]
N_pipeline_depth: int = 96  # In-flight computation depth [T4]
t_reconfig_window: float = 100e-6  # PCM full reconfiguration window (s) [T5]

# ==============================================================================
# 2.23 - 2.25 RNS ARITHMETIC, THROUGHPUT & EFFICIENCY
# ==============================================================================
m_max: int = 256  # Maximum modulus value [T5]
m_bits: int = 8  # Bit-width per residue channel [T4, T5]
k_int4: int = 1  # Tiles needed for INT4 (ceil(2*4/8)) [T5]
k_int8: int = 2  # Tiles needed for INT8 (ceil(2*8/8)) [T5]
k_int16: int = 4  # Tiles needed for INT16 (ceil(2*16/8)) [T5]
k_int32: int = 8  # Tiles needed for INT32 (ceil(2*32/8)) [T5]
k_int64: int = 16  # Tiles needed for INT64 (2 clusters of 8 QRNS tiles) [T5]
N_rrns_redundant: int = 2  # RRNS redundant moduli channels [T5]
carry_propagation: float = 0.0  # Inter-tile carry propagation delay (0 s) [T5]
max_int4_product: int = 225  # Maximum INT4 product (15*15 = 225 < 256) [T5]

# Official 8-Modulus QRNS Set (j^2 = -1 mod m)
moduli_qrns_compute: list = [241, 233, 229, 221, 205, 197, 193, 181]
roots_qrns_compute: list = [64, 89, 107, 21, 32, 14, 81, 19]
moduli_qrns_redundant: list = [173, 157]
roots_qrns_redundant: list = [80, 12]

eta_peak: float = 1.00  # Peak theoretical hardware utilization [T5]
eta_sustained: float = 0.85  # Sustained operational utilization [T5]
MAC_per_FLOPS: int = 2  # MAC to FLOPS equivalence (1 MAC = 2 FLOPS) [T5]
MAC_per_tile_raw: float = 102.4e12  # Raw per-tile MAC rate (MAC/s) [T5]
TP_int4_peak: float = 1638.4e12  # INT4 peak throughput (MAC/s) [T5]
TP_int4_sustained: float = 1392.6e12  # INT4 sustained throughput (MAC/s) [T5]
TP_int8_peak: float = 819.2e12  # INT8 peak throughput (MAC/s) [T5]
TP_int8_sustained: float = 696.3e12  # INT8 sustained throughput (MAC/s) [T5]
TP_int16_peak: float = 409.6e12  # INT16 peak throughput (MAC/s) [T5]
TP_int16_sustained: float = 348.2e12  # INT16 sustained throughput (MAC/s) [T5]
TP_int32_peak: float = 204.8e12  # INT32 peak throughput (MAC/s) [T5]
TP_int32_sustained: float = 174.1e12  # INT32 sustained throughput (MAC/s) [T5]
TP_int64_peak: float = 102.4e12  # INT64 peak throughput (MAC/s) [T5]
TP_int64_sustained: float = 87.0e12  # INT64 sustained throughput (MAC/s) [T5]
EE_int4: float = 225.7  # INT4 sustained energy efficiency (TMAC/s/W) [T5]
EE_int64: float = 14.1  # INT64 sustained energy efficiency (TMAC/s/W) [T5]

E_pcm_tier1: float = 100e-15  # Tier 1 PCM programming energy (J/switch) [T3]
E_pcm_tier2: float = 1e-12  # Tier 2 PCM programming energy (J/switch) [T3]
E_pcm_tier3: float = 10e-12  # Tier 3 PCM programming energy (J/switch) [T3]
P_reconfig_tier1: float = 1.0  # Tier 1 transient reconfig power (W) [T3]
P_reconfig_tier2: float = 10.0  # Tier 2 transient reconfig power (W) [T3]
P_reconfig_tier3: float = 100.0  # Tier 3 transient reconfig power (W) [T3]
f_delta_sparse: float = 0.01  # Sparse update fraction (<1%) [T5]
E_sparse_update: float = 0.1e-3  # Sparse update energy (<0.1 mJ) [T3]

sigma_nl_squared: float = 0.0  # Nonlinear interference power (W^2) [T1]
entropy_interchannel: float = 0.0  # Inter-channel entropy transfer [T1]
pulse_bw_constant: float = 0.44  # Transform-limited pulse-bandwidth product [T1]
delta_f_5ps: float = 88e9  # 5 ps pulse spectral width (Hz) [T1]

S_max_32x32: int = 2080800  # Max analog accumulation (32 * 255 * 255) [T5]
SNR_analog_32x32: float = 126.4  # Minimum analog SNR for 32x32 (dB) [T5]
ADC_bits_32x32: int = 21  # Equivalent ADC resolution (bits) [T5]
dB_per_bit: float = 6.02  # ADC SNR scaling constant (dB/bit) [T5]
SNR_adc_floor: float = 1.76  # ADC SNR floor offset (dB) [T5]


# ==============================================================================
def export_specs_json(output_path: str = None) -> str:
    """Exports all defined global constants to a JSON file for multi-tool interop."""
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "mini_16t_specs.json")

    registry = {}
    for k, v in list(globals().items()):
        if not k.startswith("_") and k not in [
            "json",
            "math",
            "os",
            "Dict",
            "Any",
            "export_specs_json",
            "get_k_sb2s3",
        ]:
            registry[k] = v

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    return output_path


if __name__ == "__main__":
    out = export_specs_json()
    print(
        f"[OK] Exported {len(json.load(open(out)))} global simulation constants to: {out}"
    )

n_eff_guided: float = 2.8
