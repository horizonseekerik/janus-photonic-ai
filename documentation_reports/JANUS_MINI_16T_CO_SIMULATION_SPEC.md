# PROJECT JANUS MINI (16-TILE): MULTI-PHYSICS CO-SIMULATION & SYSTEM VERIFICATION SPECIFICATION
**Document ID:** JANUS-SIM-SPEC-MINI16-2026-V1
**Target Hardware:** JANUS Mini 16-Tile Monolithic Planar MVP (Model 1A)
**Classification:** Engineering Blueprint / Verification Standard
**Lead Architect:** Deepanshu Bhardwaj
**Status:** Approved for Implementation

---

## 1. Executive Summary & Verification Objective

The objective of this specification is to define the end-to-end, multi-scale, multi-physics co-simulation framework for the **JANUS Mini 16-Tile Accelerator (Model 1A)**.

To bridge the gap between nanophotonic Maxwell field physics and high-level artificial intelligence inference, this framework couples **open-source, high-performance simulation engines** into an automated, single-command validation pipeline.

```
+---------------------------------------------------------------------------------------------------+
|                        JANUS MINI 16-TILE MULTI-SCALE VERIFICATION STACK                          |
+---------------------+-----------------------+-----------------------------------------------------+
| Simulation Tier     | Engine / Toolchain    | Primary Physical / Architectural Scope              |
+---------------------+-----------------------+-----------------------------------------------------+
| Tier 1: Optics      | 3D MEEP (FDTD)        | Maxwell solver, Sb2S3 S-matrix, field absorption |
| Tier 2: Thermal     | Elmer FEM (3D FEM)    | Transient Z-axis heat diffusion, SiO2 buffer, ROM   |
| Tier 3: Circuit     | Xyce (Parallel SPICE) | SAC2M APD, StrongARM latches, 100 GHz eye diagrams  |
| Tier 4: RTL Logic   | Cocotb + Verilator    | Gate-level CRT adder tree (210 ps), RNS encoders    |
| Tier 5: Arithmetic  | Python RNS Engine     | Spatial One-Hot, JIR scheduler, RRNS, Z3 proofs     |
+---------------------+-----------------------+-----------------------------------------------------+
```

---

## 2. Global Simulation Constants & Variable Registry

All simulation parameters defined in this section are **immutable constants** shared across all five verification tiers. Every variable is assigned a canonical **Python identifier** (used directly in simulation code), a **mathematical symbol**, a **fixed numerical value**, **SI-compatible unit**, and **tier scope** indicating which simulation tiers consume it.

**Tier Scope Key:** T1 = MEEP Optics | T2 = Elmer Thermal | T3 = Xyce Circuit | T4 = Cocotb RTL | T5 = Python RNS

---

### 2.1 Universal Physical Constants

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `c_vacuum` | c | 2.9979 x 10^8 | m/s | T1, T3 | Speed of light in vacuum |
| `h_planck` | h | 6.626 x 10^-34 | J-s | T1, T3 | Planck's constant |
| `h_bar` | h-bar | 1.0546 x 10^-34 | J-s | T1 | Reduced Planck's constant (h/2pi) |
| `k_boltzmann` | k_B | 1.381 x 10^-23 | J/K | T3 | Boltzmann constant |
| `q_electron` | q | 1.602 x 10^-19 | C | T3 | Elementary charge |
| `epsilon_0` | eps_0 | 8.854 x 10^-12 | F/m | T1, T3 | Permittivity of free space |
| `mu_0` | mu_0 | 1.2566 x 10^-6 | H/m | T1 | Permeability of free space |
| `pi` | pi | 3.14159265358979 | dimensionless | All | Mathematical constant pi |

---

### 2.2 Operating Wavelength, Laser Source & Optical Carrier

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `lambda_0` | lambda_0 | 1064 x 10^-9 | m | T1, T3 | Primary operating wavelength (Yb-fiber CW) |
| `lambda_0_nm` | lambda_0 | 1064 | nm | T1 | Operating wavelength (nanometers) |
| `f_optical` | f_0 | 281.76 x 10^12 | Hz | T1, T3 | Optical carrier frequency (c/lambda) |
| `omega_optical` | omega | 1.7703 x 10^15 | rad/s | T1 | Angular optical frequency (2*pi*f_0) |
| `E_photon` | E_ph | 1.8669 x 10^-19 | J | T1, T3 | Single photon energy (h*f_0) |
| `E_photon_eV` | E_ph | 1.1654 | eV | T1, T3 | Photon energy in electron-volts |
| `lambda_pump` | lambda_p | 976 x 10^-9 | m | T1 | Yb-fiber pump wavelength |
| `eta_qd_yb` | eta_QD | 0.917 | dimensionless | T1 | Yb quantum defect efficiency (976/1064) |
| `N_lambda` | N_lambda | 1 | dimensionless | T1 | Number of wavelength channels (single-lambda) |
| `P_ghost` | P_ghost | 0 | W | T1 | Parasitic FWM ghost power (single-lambda: 0) |

---

### 2.3 Optical Material Refractive Indices & Electro-Optic Coefficients

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `n_si` | n_Si | 3.565 | dimensionless | T1 | Silicon refractive index at 1064 nm |
| `n_sio2` | n_SiO2 | 1.444 | dimensionless | T1 | SiO2 cladding refractive index at 1064 nm |
| `n_sin` | n_SiN | 2.01 | dimensionless | T1 | Si3N4 waveguide refractive index at 1064 nm |
| `n_litao3` | n_LT | 2.13 | dimensionless | T1 | LiTaO3 refractive index at 1064 nm |
| `n_sb2s3_amorph` | n_a | 3.45 | dimensionless | T1 | Sb2S3 amorphous real refractive index |
| `k_sb2s3_amorph` | kappa_a | 0.008 | dimensionless | T1 | Sb2S3 amorphous extinction coefficient |
| `n_sb2s3_cryst` | n_c | 4.20 | dimensionless | T1 | Sb2S3 crystalline real refractive index |
| `k_sb2s3_cryst` | kappa_c | 0.18 | dimensionless | T1 | Sb2S3 crystalline extinction coefficient |
| `delta_n_pcm` | delta_n | 0.75 | dimensionless | T1 | PCM refractive index contrast (n_c - n_a) |
| `delta_n_pcm_range_max` | delta_n | 2.5 | dimensionless | T1 | Maximum observed PCM delta_n (literature) |
| `dn_dT_si` | dn/dT | 1.86 x 10^-4 | K^-1 | T1, T2 | Thermo-optic coefficient of silicon |
| `r33_litao3` | r_33 | 30.5 x 10^-12 | m/V | T1 | LiTaO3 Pockels electro-optic coefficient |
| `loss_sin_prop` | alpha_SiN | < 0.1 | dB/cm | T1 | Si3N4 waveguide propagation loss |
| `loss_litao3_prop` | alpha_LT | < 0.1 | dB/cm | T1 | LiTaO3 waveguide propagation loss |

---

### 2.4 Phase-Change Material (Sb2S3 / Sb2S3) Properties

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `T_crystallization` | T_cryst | 200 - 220 | deg-C | T1, T2 | Sb2S3 SET crystallization temperature |
| `T_melting` | T_melt | 500 - 540 | deg-C | T1, T2 | Sb2S3 RESET melting/amorphization temperature |
| `E_pcm_program` | E_PCM | 10 - 50 x 10^-12 | J | T1, T3 | PCM programming energy per device (pJ range) |
| `cycling_endurance` | N_endure | >= 10^6 | cycles | T1 | Sb2S3 switch cycling endurance floor |
| `cycling_endurance_max` | N_endure_max | 10^8 | cycles | T1 | Sb2S3 demonstrated endurance ceiling |
| `volumetric_expansion` | delta_V | 4 - 8 | % | T1, T2 | Volumetric strain (amorphous to crystalline) |
| `k_sb2s3_thermal` | k_GST | 0.5 | W/(m-K) | T2 | Sb2S3 thermal conductivity |
| `A_pcm_cell` | A_sw | 1.25 x 10^-12 | m^2 | T1, T2 | Single PCM switch footprint (1.25 um^2) |
| `V_gap_pcm` | V_gap | 25 x 10^-9 | m | T1, T2 | Nanoscale engineered void gap (> 20 nm) |
| `V_gap_minimum` | V_gap_min | 20 x 10^-9 | m | T1, T2 | Absolute minimum void gap (phonon tunneling cutoff) |
| `sb2s3_patch_thickness` | t_GST | 15 x 10^-9 | m | T1 | Sb2S3 active patch thickness (15 nm) |
| `P_pcm_static_hold` | P_hold | 0 | W | T3, T5 | Non-volatile PCM static hold power (zero) |

---

### 2.5 Waveguide & Photonic Cell Geometry

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `wg_width_si` | w_wg | 450 x 10^-9 | m | T1 | Silicon waveguide core width (450 nm) |
| `wg_height_si` | h_wg | 220 x 10^-9 | m | T1 | Silicon waveguide core height (220 nm) |
| `L_wg_phase` | L | 500 x 10^-6 | m | T1, T2 | Waveguide length for phase stability (500 um) |
| `L_wire_electrical` | L_wire | 200 x 10^-6 | m | T3, T4 | On-chip local electrical wire length (200 um) |
| `v_wire` | v_e | 1.5 x 10^8 | m/s | T3, T4 | Speed of light in on-chip metal (c/2) |
| `IL_crossing` | IL_X | 0.02 | dB | T1 | MMI waveguide crossing insertion loss per crossing |
| `XT_crossing` | XT_X | -40 | dB | T1 | MMI waveguide crossing crosstalk |

---

### 2.6 Mini 16-Tile Architectural Topology

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `N_tiles` | N_t | 16 | dimensionless | All | Number of independent residue tiles |
| `N_dim` | N_d | 32 | dimensionless | All | Matrix dimension per tile (32 x 32 mesh) |
| `N_mult_per_tile` | N_m/t | 1,024 | dimensionless | All | Multipliers per tile (N_d^2 = 32^2) |
| `N_mult_total` | N_m | 16,384 | dimensionless | All | Total optical multipliers (N_t x N_m/t) |
| `N_alphabet` | N | 256 | dimensionless | T1, T5 | Waveguide alphabet per multiplier (1-Hot 8-bit) |
| `N_alphabet_bits` | b | 8 | bits | T4, T5 | Bit-width of spatial alphabet (log2(256)) |
| `N_wg_total` | N_wg | 4,194,304 | dimensionless | T1 | Total spatial waveguides (N_m x N) |
| `S_benes` | S | 15 | stages | T1, T5 | Benes switching stages (2*log2(256) - 1) |
| `N_switch_per_mult` | N_sw/m | 1,920 | dimensionless | T1, T5 | Switches per multiplier fabric ((N/2) x S) |
| `N_switch_total` | N_sw | 31,457,280 | dimensionless | T1, T2 | Total Sb2S3 switch cells (~31.46 M) |
| `N_apd_total` | N_det | 4,194,304 | dimensionless | T3 | Total SAC2M Ge/Si APD detectors (~4.19 M) |
| `N_active_per_cycle` | N_act | 16,384 | dimensionless | T1, T3, T5 | Active photons per 10 ps cycle |
| `N_active_per_phase` | N_ph | 8,192 | dimensionless | T1, T3 | Active photons per 5 ps half-cycle phase |
| `alpha_spatial` | alpha_s | 1/256 | dimensionless | T3, T5 | Spatial activity factor (1-in-N sparsity) |
| `alpha_spatial_decimal` | alpha_s | 0.00390625 | dimensionless | T3, T5 | Decimal spatial activity factor |

---

### 2.7 Die Geometry & Z-Axis Physical Stack (Mini 16-Tile Planar)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `A_die` | A_die | 100.00 x 10^-6 | m^2 | T2 | Die footprint area (100.00 mm^2) |
| `A_die_mm2` | A_die | 100.00 | mm^2 | T2 | Die footprint area (mm^2) |
| `L_die` | L_die | 10.0 x 10^-3 | m | T2 | Die side length (10.0 mm) |
| `A_tile` | A_t | 6.25 x 10^-6 | m^2 | T2 | Individual tile area (100/16 = 6.25 mm^2) |
| `A_apd_single` | A_pd | 1.5 x 10^-12 | m^2 | T1, T3 | Single Ge/Si APD device area (1.5 um^2) |
| `h_cmos` | h_CMOS | 50 x 10^-6 | m | T2 | CMOS base substrate thickness (50 um) |
| `h_sio2_buffer` | h_ox | 250 x 10^-6 | m | T2 | SiO2 monolithic thermal buffer thickness (250 um) |
| `h_siph` | h_SiPh | 30 x 10^-6 | m | T2 | SiPh stratum thickness (30 um per stratum) |
| `N_strata` | N_str | 1 | dimensionless | T2 | SiPh strata count (Gen-1 planar monolithic) |
| `h_total_active` | T_act | 330 x 10^-6 | m | T2 | Total active die height (50+250+30 = 330 um) |
| `h_inter_stratum_sio2` | h_iox | 0 | m | T2 | Inter-stratum SiO2 spacer (N/A for Gen-1) |

---

### 2.8 Heat Spreader & Package Dimensions

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `h_hs1` | h_HS1 | 30 x 10^-6 | m | T2 | Heat Spreader 1 (dense Cu-pillar micro-matrix) |
| `h_spreader_gap` | h_gap | 50 x 10^-6 | m | T2 | Spreader gap (Cu-Cu pillar + vacuum/air void) |
| `h_hs2` | h_HS2 | 250 x 10^-6 | m | T2 | Heat Spreader 2 (external convective slim-lid) |
| `h_package_added` | h_pkg | 330 x 10^-6 | m | T2 | Total macro-package added height (HS1+gap+HS2) |
| `h_package_total` | T_pkg | 660 x 10^-6 | m | T2 | Total packaged system height (330+330 = 660 um) |
| `rho_cu_pillar_sparse` | rho_sp | 10,000 | mm^-2 | T2 | Sparse Cu-pillar density (CMOS/SiO2/SiPh) |
| `rho_cu_pillar_dense` | rho_dn | 900,000 | mm^-2 | T2 | Dense Cu-pillar density (SiPh to HS1) |
| `rho_cu_pillar_hs` | rho_hs | 950,000 | mm^-2 | T2 | HS1 to HS2 macro-package Cu-pillar density |
| `h_hbm_reference` | h_HBM | 720 x 10^-6 | m | T2 | Adjacent-die HBM memory stack height (reference) |

---

### 2.9 Thermal Material Properties -- Silicon (CMOS Substrate)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k_si_thermal` | k_Si | 148 | W/(m-K) | T2 | Silicon thermal conductivity |
| `rho_si` | rho_Si | 2,330 | kg/m^3 | T2 | Silicon mass density |
| `cp_si` | c_p,Si | 705 | J/(kg-K) | T2 | Silicon specific heat capacity |
| `alpha_si_thermal` | alpha_Si | 9.010 x 10^-5 | m^2/s | T2 | Silicon thermal diffusivity (k/rho/cp) |

---

### 2.10 Thermal Material Properties -- SiO2 (Thermal Buffer)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k_sio2_thermal` | k_ox | 1.38 | W/(m-K) | T2 | SiO2 fused silica thermal conductivity |
| `rho_sio2` | rho_ox | 2,200 | kg/m^3 | T2 | SiO2 mass density |
| `cp_sio2` | c_p,ox | 703 | J/(kg-K) | T2 | SiO2 specific heat capacity |
| `alpha_sio2` | alpha_ox | 9.05 x 10^-7 | m^2/s | T2 | SiO2 thermal diffusivity (k/rho/cp) |
| `m_sio2_buffer` | m_ox | 5.500 x 10^-5 | kg | T2 | SiO2 buffer mass (A_die x h_ox x rho_ox) |
| `C_sio2_buffer` | C_ox | 38.66 x 10^-3 | J/K | T2 | SiO2 buffer heat capacity (m_ox x c_p,ox) |

---

### 2.11 Thermal Material Properties -- Copper (TDVs, Heat Spreaders)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k_cu` | k_Cu | 400 | W/(m-K) | T2 | Copper thermal conductivity |
| `rho_cu` | rho_Cu | 8,960 | kg/m^3 | T2 | Copper mass density |
| `cp_cu` | c_p,Cu | 385 | J/(kg-K) | T2 | Copper specific heat capacity |
| `alpha_cu` | alpha_Cu | 1.160 x 10^-4 | m^2/s | T2 | Copper thermal diffusivity |

---

### 2.12 Thermal Material Properties -- Germanium (APD Absorption Layer)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k_ge` | k_Ge | 60 | W/(m-K) | T2 | Germanium thermal conductivity |
| `rho_ge` | rho_Ge | 5,323 | kg/m^3 | T2 | Germanium mass density |
| `cp_ge` | c_p,Ge | 320 | J/(kg-K) | T2 | Germanium specific heat capacity |
| `alpha_ge` | alpha_Ge | 3.52 x 10^-5 | m^2/s | T2 | Germanium thermal diffusivity |

---

### 2.13 Thermal Material Properties -- Air (Package Voids)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k_air` | k_air | 0.026 | W/(m-K) | T2 | Air thermal conductivity (54x lower than SiO2) |

---

### 2.14 Thermal Material Properties -- LiTaO3 (Pockels Modulators)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `k_litao3` | k_LT | 4.6 | W/(m-K) | T2 | LiTaO3 thermal conductivity |
| `rho_litao3` | rho_LT | 7,456 | kg/m^3 | T2 | LiTaO3 mass density |
| `cp_litao3` | c_p,LT | 424 | J/(kg-K) | T2 | LiTaO3 specific heat capacity |

---

### 2.15 Thermal Dynamics, JIR Scheduling & Temperature Budgets

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `T_ambient` | T_amb | 298.15 | K | T2 | Ambient reference temperature (25 deg-C) |
| `T_ambient_C` | T_amb | 25.0 | deg-C | T2 | Ambient reference temperature (Celsius) |
| `tau_diff` | tau_diff | 69.06 x 10^-3 | s | T2, T5 | SiO2 thermal diffusion time (h_ox^2 / alpha_ox) |
| `tau_diff_ms` | tau_diff | 69.06 | ms | T2, T5 | Thermal diffusion time (milliseconds) |
| `tau_jir` | tau_JIR | 5.0 x 10^-6 | s | T2, T5 | JIR activation cycle duration (5 us) |
| `tau_jir_us` | tau_JIR | 5.0 | us | T2, T5 | JIR activation cycle (microseconds) |
| `N_jir_per_tau_diff` | N_JIR | 13,812 | cycles | T2, T5 | JIR cycles per thermal diffusion time |
| `t_jir_rotation` | t_rot | 4.0 x 10^-6 | s | T5 | JIR state-transition rotation overhead (4 us) |
| `Q_gen_per_jir` | Q_gen | 30.85 x 10^-6 | J | T2, T5 | Heat generated per JIR cycle (P_total x tau_JIR) |
| `delta_T_cycle` | dT_cyc | 0.798 x 10^-3 | K | T2, T5 | Per-cycle thermal transient rise (Q_gen / C_ox) |
| `delta_T_cycle_mK` | dT_cyc | 0.798 | mK | T2, T5 | Per-cycle thermal rise (millikelvin) |
| `delta_T_crit_phase` | dT_crit | 5.72 | K | T1, T2 | Phase-drift critical temperature rise |
| `delta_T_steady` | dT_ss | 0.213 | K | T2 | Steady-state SiPh temperature rise above ambient |
| `thermal_margin_ratio` | M_th | 26.9 | dimensionless | T2 | Thermal stability margin (dT_crit / dT_ss) |
| `T_max_operating` | T_op,nom | 70.0 | deg-C | T2, T5 | Nominal commercial operating ceiling (JIR rotation trigger @ 63 deg-C) |
| `T_retention_max` | T_ret,max | 100.0 | deg-C | T2, T5 | Hard physical 10-year Sb2S3 non-volatile retention limit (fail-safe gate) |
| `T_crystallization_guard` | T_cryst | 150.0 | deg-C | T2 | Physical Sb2S3 amorphous-to-crystalline phase transition onset |
| `R_th_down` | R_down | 0.195 | K/W | T2 | Downward CMOS-SiO2 thermal resistance (100 mm^2) |
| `R_th_up` | R_up | 0.552 | K/W | T2 | Upward SiPh-HS1 thermal resistance (100 mm^2) |
| `P_per_tile` | P_t | 0.386 | W | T2, T5 | Average power dissipation per tile |
| `delta_T_permissible_siph` | dT_perm | 0.048 | K | T1, T2 | Permissible SiPh thermal stability window |

---

### 2.16 SAC2M Ge/Si Avalanche Photodetector Parameters

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `M_apd` | M | 7 | dimensionless | T3 | APD avalanche multiplication gain |
| `k_ionization` | k | 0.06 | dimensionless | T3 | Effective impact ionization ratio |
| `F_excess_noise` | F(M) | 2.0 | dimensionless | T3 | McIntyre excess noise factor at M=7, k=0.06 |
| `R_responsivity` | R | 0.8 | A/W | T3 | Germanium responsivity at 1064 nm |
| `f_3db_apd` | f_3dB | 105 x 10^9 | Hz | T3 | APD 3 dB electrical bandwidth (105 GHz) |
| `GBP_apd` | GBP | 441 x 10^9 | Hz | T3 | Gain-bandwidth product (M x f_3dB) |
| `t_pd_clearance` | t_PD | 1.52 x 10^-12 | s | T3 | Photogenerated carrier clearance time (1.52 ps) |
| `C_j_apd` | C_j | 0.8 x 10^-15 | F | T3 | APD junction capacitance (0.8 fF) |
| `R_s_apd` | R_s | 25 | ohm | T3 | APD series resistance (25 ohm) |
| `C_int_parasitic` | C_int | 3.0 x 10^-15 | F | T3 | Maximum parasitic input capacitance (3 fF) |
| `I_dark_apd` | I_dark | < 10^-9 | A | T3 | APD dark current upper bound (< 1 nA) |

---

### 2.17 Receiver Electronics & Decision Logic

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sigma_tia` | sigma_TIA | 1.8 x 10^-6 | A | T3 | TIA input-referred RMS noise current (1.8 uA) |
| `E_strongarm` | E_SA | 100 x 10^-18 | J | T3, T4 | StrongARM per-decision energy (100 aJ = 0.1 fJ) |
| `t_regen` | t_reg | 3.5 x 10^-12 | s | T3, T4 | StrongARM regeneration time (<=3.5 ps) |
| `E_pockels_switch` | E_Pock | 50 x 10^-18 | J | T1, T3 | Pockels electro-optic switch energy (50 aJ) |

---

### 2.18 Receiver Sensitivity, BER & Detection Margin

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `BER_target` | BER | 10^-18 | dimensionless | T3, T5 | Target bit error rate (<1 error per century @ 100 GHz) |
| `Q_factor` | Q | 9.38 | dimensionless | T3 | Q-factor for BER=10^-18 (erfc inverse) |
| `P_sens_theoretical` | P_sens,th | 3.01 x 10^-6 | W | T3 | Theoretical receiver sensitivity (3.01 uW) |
| `P_sens_theoretical_dbm` | P_sens,th | -25.21 | dBm | T3 | Theoretical sensitivity in dBm |
| `sensitivity_margin_db` | M_sens | 2.0 | dB | T3 | Engineering margin added to theoretical sensitivity |
| `P_sens_practical` | P_sens | 4.79 x 10^-6 | W | T3 | Practical receiver sensitivity (4.79 uW) |
| `P_sens_practical_dbm` | P_sens | -23.21 | dBm | T3 | Practical sensitivity in dBm (-25.21 + 2.0) |
| `P_det` | P_det | 13.82 x 10^-6 | W | T3 | Delivered signal power at detector (13.82 uW) |
| `P_det_dbm` | P_det | -18.59 | dBm | T3 | Delivered power in dBm |
| `link_margin` | M_link | +4.61 | dB | T3 | Net binary detection margin (P_det - P_sens) |
| `link_margin_linear` | M_link | 2.89 | dimensionless | T3 | Linear power safety factor (10^(4.61/10)) |
| `P_false_positive` | P_FP | 2.55 x 10^-16 | dimensionless | T3, T5 | Dark-channel false positive probability (255 x BER) |

---

### 2.19 Laser Optical Power & Electrical Power (Mini 16-Tile)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `P_laser_optical` | P_opt | 2.21 | W | T1, T3 | Master laser CW optical launch power |
| `P_laser_optical_dbm` | P_opt | +33.44 | dBm | T1, T3 | Laser optical power in dBm |
| `WPE` | eta_WPE | 0.75 | dimensionless | T3 | Laser wall-plug efficiency (>75%) |
| `P_laser_electrical` | P_elec | 2.95 | W | T3 | Laser electrical consumption (P_opt / WPE) |

---

### 2.20 Optical Distribution Loss Budget (Mini 16-Tile)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `N_mmi_stages` | N_MMI | 13 | stages | T1 | Cascaded 1:2 MMI splitter count (log2(8192)) |
| `L_split_per_stage` | L_sp | 3.0103 | dB | T1 | Ideal per-stage splitting loss (10*log10(2)) |
| `L_split_ideal` | L_sp,tot | 39.13 | dB | T1 | Total ideal passive splitting loss (13 x 3.0103) |
| `L_mmi_excess_per_stage` | L_MMI | 0.30 | dB/stage | T1 | MMI excess insertion loss per stage |
| `L_mmi_excess_total` | L_MMI,tot | 3.90 | dB | T1 | Total MMI excess loss (13 x 0.30) |
| `L_benes_per_stage` | L_B | 0.50 | dB/stage | T1 | Dilated Benes routing loss per stage |
| `L_benes_total` | L_B,tot | 7.50 | dB | T1 | Total 15-stage Benes loss (15 x 0.50) |
| `L_propagation_coupling` | L_prop | 1.50 | dB | T1 | Waveguide propagation & interlayer coupling |
| `L_excess_total` | L_ex | 12.90 | dB | T1 | Total excess path loss (MMI + Benes + prop) |
| `L_distribution_total` | L_tot | 52.03 | dB | T1, T3 | Total end-to-end distribution loss (ideal + excess) |
| `IL_switch_cell` | IL_sw | 0.10 | dB/cell | T1 | Sb2S3 switch cell insertion loss (a-Sb2S3 state) |
| `ER_dilated_benes` | ER | 25.0 | dB | T1 | Dilated Benes extinction ratio (minimum) |

---

### 2.21 System Electrical Power Budget (Mini 16-Tile)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `P_laser_elec` | P_1 | 2.95 | W | T3 | 1064 nm Yb laser (75% WPE) electrical power |
| `P_litao3_routers` | P_2 | 0.51 | W | T3 | LiTaO3 Pockels micro-ring router power |
| `P_apd_detectors` | P_3 | 0.16 | W | T3 | Ge/Si SAC2M APD detector array power (M=7) |
| `P_optical_amp` | P_4 | 0.00 | W | T3 | Optical amplification layer (eliminated = 0 W) |
| `P_pcm_static` | P_5 | 0.00 | W | T3 | PCM routing switch static hold (non-volatile = 0 W) |
| `P_cmos_logic` | P_6 | 1.05 | W | T3, T4 | CMOS encoders / adders / CRT reconstruction |
| `P_jir_control` | P_7 | 1.50 | W | T4, T5 | JIR scheduler and control logic |
| `P_total_system` | P_sys | 6.17 | W | All | Total full-system electrical power |

---

### 2.22 Timing, Frequency & Latency Budget

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `f_clk` | f_clk | 100 x 10^9 | Hz | All | System operating clock frequency (100 GHz) |
| `T_cycle` | T_cyc | 10.0 x 10^-12 | s | All | Wave-pipelined clock cycle period (10.0 ps) |
| `T_phase` | T_ph | 5.0 x 10^-12 | s | T1, T3 | Time-multiplexed illumination phase duration (5 ps) |
| `tau_fwhm_min` | tau_min | 3.0 x 10^-12 | s | T1 | Minimum optical pulse FWHM (3 ps) |
| `tau_fwhm_max` | tau_max | 5.0 x 10^-12 | s | T1 | Maximum optical pulse FWHM (5 ps) |
| `t_mod` | t_mod | 10.0 x 10^-12 | s | T1, T3 | Electro-optic injection pulse interval (<=10 ps) |
| `t_pd` | t_PD | 1.52 x 10^-12 | s | T3 | Photodetector carrier clearance (1.52 ps) |
| `t_wire` | t_wire | 1.33 x 10^-12 | s | T3, T4 | Electrical wire interconnect delay (L_wire/v_e) |
| `t_guard` | t_guard | 3.5 x 10^-12 | s | T1, T3 | Inter-pulse guard margin (ISI isolation) |
| `t_opt_benes` | t_opt | 750 x 10^-12 | s | T1 | 15-stage Benes optical propagation delay (750 ps) |
| `t_crt` | t_CRT | 210 x 10^-12 | s | T4 | CRT adder-tree accumulation delay (210 ps) |
| `N_crt_pipeline_stages` | S_CRT | 4 | stages | T4 | CRT pipelined adder tree stage count |
| `T_latency_total` | T_lat | 963 x 10^-12 | s | T1-T4 | Total end-to-end single-op latency (963 ps) |
| `N_pipeline_depth` | D_pipe | 96 | stages | T4 | Wave-pipelined in-flight computation depth |
| `t_reconfig_window` | t_cfg | 100 x 10^-6 | s | T5 | PCM full-weight reconfiguration window (0.1 ms) |

---

### 2.23 RNS Arithmetic & Moduli Configuration

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `m_max` | m_max | 256 | dimensionless | T5 | Maximum modulus value (fits 256-waveguide alphabet) |
| `m_bits` | b_m | 8 | bits | T4, T5 | Bit-width per residue channel (log2(m_max)) |
| `k_int4` | k_4 | 1 | tiles | T5 | Tiles needed for INT4 (ceil(2*4/8)) |
| `k_int8` | k_8 | 2 | tiles | T5 | Tiles needed for INT8 (ceil(2*8/8)) |
| `k_int16` | k_16 | 4 | tiles | T5 | Tiles needed for INT16 (ceil(2*16/8)) |
| `k_int32` | k_32 | 8 | tiles | T5 | Tiles needed for INT32 (ceil(2*32/8)) |
| `k_int64` | k_64 | 16 | tiles | T5 | Tiles needed for INT64 (2 clusters of 8 PRNS tiles (Hybrid Partitioning)) |
| `N_rrns_redundant` | r | 2 | channels | T5 | RRNS redundant moduli channels for fault detection |
| `carry_propagation` | t_carry | 0 | s | T5 | Inter-tile carry propagation delay (spatial: zero) |
| `max_int4_product` | Z_4 | 225 | dimensionless | T5 | Maximum INT4 product (15 x 15 = 225 < 256) |

---

### 2.24 Throughput & Energy Efficiency (Mini 16-Tile)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `eta_peak` | eta_pk | 1.00 | dimensionless | T5 | Peak theoretical hardware utilization (100%) |
| `eta_sustained` | eta_su | 0.85 | dimensionless | T5 | Sustained operational utilization (85%) |
| `MAC_per_FLOPS` | - | 2 | FLOPS/MAC | T5 | MAC to FLOPS equivalence (1 MAC = 2 FLOPS) |
| `MAC_per_tile_raw` | M_t | 102.4 x 10^12 | MAC/s | T5 | Raw per-tile MAC rate (N_d^2 x f_clk) |
| `TP_int4_peak` | TP_4p | 1,638.4 x 10^12 | MAC/s | T5 | INT4 peak throughput (16 tiles x MAC_t) |
| `TP_int4_sustained` | TP_4s | 1,392.6 x 10^12 | MAC/s | T5 | INT4 sustained throughput (peak x 0.85) |
| `TP_int8_peak` | TP_8p | 819.2 x 10^12 | MAC/s | T5 | INT8 peak throughput (16/2 x MAC_t) |
| `TP_int8_sustained` | TP_8s | 696.3 x 10^12 | MAC/s | T5 | INT8 sustained throughput |
| `TP_int16_peak` | TP_16p | 409.6 x 10^12 | MAC/s | T5 | INT16 peak throughput (16/4 x MAC_t) |
| `TP_int16_sustained` | TP_16s | 348.2 x 10^12 | MAC/s | T5 | INT16 sustained throughput |
| `TP_int32_peak` | TP_32p | 204.8 x 10^12 | MAC/s | T5 | INT32 peak throughput (16/8 x MAC_t) |
| `TP_int32_sustained` | TP_32s | 174.1 x 10^12 | MAC/s | T5 | INT32 sustained throughput |
| `TP_int64_peak` | TP_64p | 102.4 x 10^12 | MAC/s | T5 | INT64 peak throughput (16/16 x MAC_t) |
| `TP_int64_sustained` | TP_64s | 87.0 x 10^12 | MAC/s | T5 | INT64 sustained throughput |
| `EE_int4` | EE_4 | 225.7 | TMAC/s/W | T5 | INT4 sustained energy efficiency |
| `EE_int64` | EE_64 | 14.1 | TMAC/s/W | T5 | INT64 sustained energy efficiency |

---

### 2.25 PCM Reconfiguration & Transient Power

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `E_pcm_tier1` | E_cfg1 | 100 x 10^-15 | J/switch | T3 | Tier 1 PCM programming energy (~100 fJ) |
| `E_pcm_tier2` | E_cfg2 | 1 x 10^-12 | J/switch | T3 | Tier 2 PCM programming energy (~1 pJ) |
| `E_pcm_tier3` | E_cfg3 | 10 x 10^-12 | J/switch | T3 | Tier 3 PCM programming energy (~10 pJ) |
| `P_reconfig_tier1` | P_cfg1 | 1 | W | T3 | Tier 1 transient reconfig power (10^9 switches @ 0.1 ms) |
| `P_reconfig_tier2` | P_cfg2 | 10 | W | T3 | Tier 2 transient reconfig power |
| `P_reconfig_tier3` | P_cfg3 | 100 | W | T3 | Tier 3 transient reconfig power (conservative) |
| `f_delta_sparse` | f_delta | < 0.01 | dimensionless | T5 | Sparse incremental update fraction (<1%) |
| `E_sparse_update` | E_sp | < 0.1 x 10^-3 | J | T3 | Sparse incremental energy per update (<0.1 mJ) |

---

### 2.26 Nonlinear Optics & Spectral Purity

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sigma_nl_squared` | sigma_NL^2 | 0 | W^2 | T1 | Nonlinear interference power (single-lambda: 0) |
| `entropy_interchannel` | E_ij | 0 | dimensionless | T1 | Inter-channel entropy transfer (single-lambda: 0) |
| `pulse_bw_constant` | K_TBP | 0.44 | dimensionless | T1 | Transform-limited pulse-bandwidth product |
| `delta_f_5ps` | delta_f | 88 x 10^9 | Hz | T1 | 5 ps pulse spectral width (0.44/5ps = 88 GHz) |

---

### 2.27 Analog SNR & Precision Limits (Reference Comparisons)

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `S_max_32x32` | S_max | 2,080,800 | levels | T5 | Max analog accumulation (32 x 255 x 255) |
| `SNR_analog_32x32` | SNR_A | 126.4 | dB | T5 | Minimum analog SNR for 32x32 (20*log10) |
| `ADC_bits_32x32` | N_ADC | 21 | bits | T5 | Equivalent ADC resolution (log2 of S_max) |
| `dB_per_bit` | - | 6.02 | dB/bit | T5 | ADC quantization SNR scaling constant |
| `SNR_adc_floor` | - | 1.76 | dB | T5 | ADC SNR floor offset in SNR = 6.02N + 1.76 |
| `temporal_slicing_penalty` | S_slice | 6 | cycles/MAC | T5 | 23-bit sliced into 4-bit: 6 cycles per MAC |

---

### 2.28 Logarithmic & Unit Conversion Constants

| Python Variable | Symbol | Value | Unit | Tier Scope | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dB_per_split` | - | 3.0103 | dB | T1 | Power per 1:2 split (10*log10(2)) |
| `mW_to_dBm_offset` | - | 0 | dBm | T3 | dBm reference: 0 dBm = 1 mW |

---

## 3. Target Hardware Baseline: JANUS Mini 16-Tile (Model 1A)

The simulation suite strictly targets the verified hardware parameters of the **JANUS Mini 16-Tile Planar Monolithic Accelerator**:

| Architectural Parameter | Physical Value | Engineering Unit / Notes |
| :--- | :--- | :--- |
| **Residue Tile Count (N_tiles)** | 16 | Independent optical residue tiles |
| **Tile Matrix Mesh (N_dim)** | 32 x 32 | Matrix dimensions per tile |
| **Multipliers per Tile** | 1,024 | 32^2 optical multiplier fabrics |
| **Total Optical Multipliers** | **16,384** | 16 tiles x 1,024 multipliers |
| **Waveguide Alphabet per Multiplier** | 256 | One-Hot 8-bit residue spatial channels |
| **Total Spatial Waveguides** | **4,194,304** | 16,384 x 256 spatial channels |
| **Benes Switching Stages (S)** | 15 stages | 2*log2(256) - 1 universal topology |
| **Switches per Multiplier Fabric** | 1,920 | (256/2) x 15 non-volatile cells |
| **Total Sb2S3 Switch Cells** | **31,457,280** | ~31.46 Million non-volatile cells (0 W hold) |
| **Terminal Ge/Si SAC2M APDs** | **4,194,304** | ~4.19 Million monolithic pixels |
| **Active Photons per 10 ps Cycle** | 16,384 | 1-in-256 spatial sparsity (8,192 per 5 ps phase) |
| **Operating Frequency** | **100 GHz** | T_cycle = 10.0 ps wave-pipelined |
| **Die Footprint (A_die)** | **100.00 mm^2** | 10.0 mm x 10.0 mm monolithic planar |
| **Total Active Die Height** | **330 um** | 50 um CMOS + 250 um SiO2 + 30 um SiPh |
| **Master Laser Launch Power** | **2.21 W Optical CW** | 1064 nm Yb-fiber CW (+33.44 dBm) |
| **Master Laser Electrical Power** | **2.95 W Electrical** | >75% Wall-Plug Efficiency (WPE) |
| **Total System Electrical Power** | **6.17 W** | Full chip power under continuous load |
| **Sustained INT4 Throughput (eta=0.85)** | **1,392.6 TMAC/s** | 225.7 TMAC/s/W energy efficiency |
| **Sustained INT64 Throughput (eta=0.85)** | **87.0 TMAC/s** | 14.1 TMAC/s/W energy efficiency |

---

## 4. Five-Tier Multi-Physics Co-Simulation Pipeline

```
+---------------------------------------------------------------------------------------------------+
|                        JANUS MINI 16-TILE DATA HANDOFF & SIMULATION FLOW                          |
+---------------------------------------------------------------------------------------------------+

   [ TIER 1: 3D MEEP FDTD ]
   | - Solves Sb2S3 cell (a-Sb2S3 vs c-Sb2S3), TFLN crossing, and 1x256 Pockels router
   | - Exports: S-parameters (Touchstone format) & Volumetric Optical Absorption Q_opt(x,y,z)
   v
   +-- S-Parameters (Touchstone .s4p) ----------+
   |                                            v
   |                                 [ TIER 3: XYCE SPICE ]
   |                                 | - Vector-fitting (vectfit) to passive subcircuit
   |                                 | - SAC2M APD equivalent circuit (M=7, C_j=0.8 fF)
   |                                 | - StrongARM dynamic latch model (~100 aJ/event)
   |                                 | - Outputs: 100 GHz Eye Diagrams, Jitter, BER <= 10^-18
   v                                 v
   [ TIER 2: ELMER FEM THERMAL ]     | Realistic BER & Transit Delays
   | - 3D transient heat diffusion   |
   | - Imports Q_opt(x,y,z) + CMOS   |
   | - Validates tau_diff = 69.06 ms |
   | - Exports: Reduced-Order Model  |
   v                                 |
   +-- Dynamic Thermal ROM Matrix ---+-----------------------------+
   |                                 v                             v
   |              [ TIER 4: DIGITAL RTL (COCOTB + VERILATOR) ]     |
   |              | - Gate-level RNS Modulo Front-End               |
   |              | - Pipelined CRT Adder Tree (210 ps)             |
   |              | - Evaluates CMOS propagation & clock power       |
   |              v                                                |
   |              +-- Gate Delays & Latency -----------------------+
   |                                                               v
   +-----------------------------------------------------> [ TIER 5: PYTHON RNS ENGINE ]
                                                           | - Spatial One-Hot Tensor Routing
                                                           | - JIR Dynamic Thermal Scheduler
                                                           | - RRNS Fault Self-Healing
                                                           | - Z3 SMT Formal Proofs
                                                           | - Exact INT4-INT64 GEMM Benchmarking
                                                           v
                                                           [ VERIFIED EXACT ACCELERATOR ]
```

---

### Tier 1: Electro-Optics & FDTD Extraction (3D MEEP)

#### A. Target Unit-Cell Geometries
1. **Sb2S3 Phase-Change Directional Coupler Switch:**
   - Silicon core (wg_width_si=450 nm x wg_height_si=220 nm), SiO2 cladding (n_sio2=1.444).
   - Active Sb2S3 patch (sb2s3_patch_thickness=15 nm, A_pcm_cell=1.25 um^2 relaxed cell area).
   - Solves at lambda_0=1064 nm in both states:
     - **Amorphous (a-Sb2S3):** n_sb2s3_amorph=3.45 + i*k_sb2s3_amorph=0.008 (Low-loss cross state).
     - **Crystalline (c-Sb2S3):** n_sb2s3_cryst=4.20 + i*k_sb2s3_cryst=0.18 (High-index bar state).
2. **Ultra-Low-Loss Waveguide Crossing Matrix:**
   - Multi-mode interference (MMI) optimized crossing (IL_crossing < 0.02 dB, XT_crossing < -40 dB).
3. **LiTaO3 Pockels Input Modulator Cell:**
   - Thin-film lithium tantalate (r33_litao3=30.5 pm/V) with sub-E_pockels_switch=50 aJ/switch energy.

#### B. Extracted Deliverables
* **Scattering Matrix (Touchstone `.s4p` format):** Insertion loss (IL_switch_cell <= 0.10 dB), extinction ratio (ER_dilated_benes >= 25 dB), phase response, and group delay.
* **Volumetric Heat Density Map (Q_opt(x,y,z)):** Exported to HDF5 grid using the formula:
  Q_opt(x,y,z) = (1/2) * omega_optical * epsilon_0 * Im[eps_r(x,y,z)] * |E(x,y,z)|^2

---

### Tier 2: 3D Multi-Stratum Thermal Stack Analysis (Elmer FEM)

#### A. Geometric Domain & Material Properties
* **CMOS Base Substrate:** h_cmos=50 um Silicon (k_si_thermal=148 W/(m-K), rho_si=2330 kg/m^3, cp_si=705 J/(kg-K)).
* **Monolithic SiO2 Thermal Buffer:** h_sio2_buffer=250 um fused silica (k_sio2_thermal=1.38 W/(m-K), rho_sio2=2200 kg/m^3, cp_sio2=703 J/(kg-K), alpha_sio2=9.05 x 10^-7 m^2/s).
* **SiPh Core Stratum:** h_siph=30 um active photonics + Cu Through-Dielectric Vias (TDVs).
* **Boundary Conditions:** Top surface convection/conduction to Heat Spreader (HS1, T_ambient=25 deg-C), lateral adiabatic boundaries.

#### B. Verification Targets
1. **Thermal Diffusion Time Constant:** Verify tau_diff = h_sio2_buffer^2 / alpha_sio2 = 69.06 ms = 13,812 JIR cycles.
2. **Per-Cycle Thermal Rise:** Verify delta_T_cycle <= 0.80 mK per tau_jir=5 us JIR computational epoch.
3. **Non-Volatile Retention Guard:** Ensure T_max_operating < 70 deg-C (much less than T_crystallization_guard=150 deg-C).
4. **Thermal ROM Extraction:** Export state-space Foster/Cauer RC thermal impedance matrices for the Python JIR scheduler.

---

### Tier 3: Circuit & Signal Integrity Co-Simulation (Xyce SPICE)

#### A. Subcircuit Network Composition
1. **Passive Optical Backbone:** MEEP S-parameter Touchstone files fitted to passive, causal SPICE subcircuits using rational vector-fitting (vectfit).
2. **SAC2M Ge/Si Avalanche Photodetector:**
   - Equivalent circuit with primary photocurrent I_ph = R_responsivity * P_opt (R_responsivity=0.8 A/W at lambda_0=1064 nm).
   - Avalanche gain multiplication M_apd=7.
   - Junction capacitance C_j_apd=0.8 fF, series resistance R_s_apd=25 ohm.
   - Excess noise factor F_excess_noise=2.0 with ionization ratio k_ionization=0.06.
3. **StrongARM Regenerative Comparator:**
   - Clocked sensing latch consuming E_strongarm=100 aJ/event, regeneration time t_regen <= 3.5 ps.

#### B. Verification Targets
1. **Eye Diagram Opening:** Open eye at f_clk=100 GHz optical rate (T_cycle=10 ps cycle period).
2. **Bit Error Rate (BER):** Verify BER_target <= 10^-18 under practical sensitivity P_sens_practical=-23.21 dBm with link_margin=+4.61 dB at P_det=-18.59 dBm.

---

### Tier 4: Digital CMOS RTL & Timing Verification (Cocotb + Verilator)

#### A. Synthesized Digital Blocks
1. **High-Speed RNS Modulo Front-End:** Decomposes input integers X into x_i = X mod m_i across N_tiles=16 parallel residue channels (m_i <= m_max=256).
2. **Pipelined Chinese Remainder Theorem (CRT) Adder Tree:**
   - N_crt_pipeline_stages=4 stage pipelined modulo adder tree reconstructing 64-bit integer values from 16 residue channels.
   - Total digital reconstruction latency t_crt <= 210 ps.
3. **JIR Consistency & Fault Monitor:** Monitors strongARM column outputs for RRNS parity violations.

#### B. Verification Targets
* Cycle-accurate co-simulation linking Python testbenches to compiled Verilog logic with zero clock cycle slips.

---

### Tier 5: Algorithmic Exactness, JIR & RRNS Verification (Python Engine)

#### A. Core Python Modules
1. **`moduli_generator.py`:** Generates coprime sets M = {m_1, ..., m_16} with m_i <= m_max=256, satisfying dynamic range prod(m_i) > 2^64.
2. **`formal_verifier.py`:** Uses the **Z3 SMT Solver** to mathematically prove that finite field multiplication in Z_(m_i) is isomorphic to the Benes permutation states without edge-case failures.
3. **`one_hot_router.py`:** Simulates spatial 1-hot tensor contractions (N_dim=32 x 32 matrices across N_tiles=16 tiles) with zero floating-point rounding.
4. **`jir_scheduler.py`:** Emulates microsecond-level closed-loop tile temperature tracking using the Elmer thermal ROM matrix, executing dynamic tile rotation within tau_jir=5 us.
5. **`rrns_fault_engine.py`:** Injects stochastic physical bit errors (from Xyce BER models) and executes single-channel residue projection self-healing with N_rrns_redundant=2 redundant channels.
6. **`gemm_validator.py`:** Executes standard INT4, INT8, INT16, INT32, INT64 matrix multiplication benchmarks and performs bit-exact comparison against NumPy / PyTorch 64-bit ground truth.

---

## 5. Quantitative Pass / Fail Verification Criteria

To achieve full engineering sign-off for the JANUS Mini 16-Tile model, the unified simulation suite must satisfy the following numerical bounds:

| Verification Metric | Target Requirement | Strict Pass / Fail Threshold |
| :--- | :--- | :--- |
| **Sb2S3 Insertion Loss (a-Sb2S3)** | IL_switch_cell <= 0.10 dB/cell | **PASS if IL <= 0.10 dB** |
| **Dilated Benes Extinction Ratio** | ER_dilated_benes >= 25.0 dB | **PASS if ER >= 25.0 dB** |
| **Waveguide Crossing Insertion Loss** | IL_crossing <= 0.02 dB/crossing | **PASS if IL <= 0.02 dB** |
| **Waveguide Crossing Crosstalk** | XT_crossing <= -40.0 dB | **PASS if XT <= -40.0 dB** |
| **SiO2 Thermal Diffusion Time** | tau_diff = 69.06 ms | **PASS if 65 ms <= tau_diff <= 72 ms** |
| **Per-Cycle Thermal Transient** | delta_T_cycle <= 0.80 mK | **PASS if dT <= 0.80 mK** |
| **Max Steady-State Operating Temp** | <= T_max_operating = 70 deg-C | **PASS if T_steady < 100 deg-C** |
| **APD Practical Sensitivity Margin** | link_margin >= +4.61 dB | **PASS if Margin >= +4.00 dB** |
| **Optical Receiver Bit Error Rate** | BER_target <= 10^-18 | **PASS if BER <= 10^-18** |
| **CRT Adder Tree Digital Latency** | t_crt <= 210 ps | **PASS if t_CRT <= 220 ps** |
| **RRNS Single-Fault Correction** | 100.0% Recovery | **PASS if Error Correction = 100.0%** |
| **Arithmetic GEMM Precision Error** | **0.00000000000000%** | **PASS if Numerical Deviation = 0** |

---

## 6. Directory Architecture & Modular Workspace Layout

```
janus_mini16_sim/
+-- configs/
|   +-- mini_16t_constants.py         # ALL Section 2 global variables as Python constants
|   +-- mini_16t_specs.json           # JSON export of constants for cross-tool interop
+-- tier1_meep_optics/
|   +-- sb2s3_switch_cell.py         # 3D FDTD of PCM directional coupler
|   +-- waveguide_crossing.py         # MMI crossing extraction
|   +-- litao3_pockels_router.py      # LiTaO3 Pockels micro-ring modulator
|   +-- export_touchstone.py          # Generates Touchstone .s4p files
|   +-- export_heat_map.py            # Exports Q_opt(x,y,z) to HDF5
+-- tier2_elmer_thermal/
|   +-- mini16_mesh.geo               # Gmsh 3D stack geometry (330 um)
|   +-- materials.sif                 # Elmer material property definitions
|   +-- case.sif                      # Elmer solver input file (transient heat)
|   +-- extract_thermal_rom.py        # Extracts Foster/Cauer RC network
+-- tier3_xyce_circuit/
|   +-- vector_fit_s_params.py        # Rational fitting for SPICE subcircuits
|   +-- sac2m_apd_model.cir           # Ge/Si SAC2M equivalent circuit
|   +-- strongarm_latch.cir           # StrongARM regenerative comparator
|   +-- run_eye_diagram.cir           # 100 GHz transient eye diagram & BER
+-- tier4_rtl_digital/
|   +-- rns_encoder.v                 # Modulo decomposition logic
|   +-- crt_adder_tree.v              # 210 ps pipelined CRT reconstruction
|   +-- jir_fault_monitor.v           # RRNS parity violation detector
|   +-- test_crt_cocotb.py            # Cocotb testbench with Verilator
+-- tier5_python_rns/
|   +-- moduli_generator.py           # 16-channel coprime dynamic range
|   +-- formal_verifier.py            # Z3 SMT formal proof
|   +-- spatial_one_hot_router.py     # 15-stage Benes tensor contraction
|   +-- jir_thermal_scheduler.py      # Microsecond tile rotation engine
|   +-- rrns_self_healing.py          # Single-fault parity recovery
|   +-- gemm_exact_benchmark.py       # Bit-exact GEMM validation vs FP32/INT64
+-- run_mini16_full_cosim.py          # Master orchestrator executing Tiers 1-5
+-- README.md                         # Setup instructions & dependencies
```

---
*Specification approved for Project JANUS Mini 16-Tile hardware realization and validation suite execution.*