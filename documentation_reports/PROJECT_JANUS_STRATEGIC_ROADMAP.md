# PROJECT JANUS: STRATEGIC HARDWARE ENGINEERING & PRODUCT COMMERCIALIZATION ROADMAP
**Classification:** Proprietary / Engineering Blueprint  
**Patent Application Reference:** Indian Patent App No. 202611052791 (Patent Pending)  
**Lead Architect:** Deepanshu Bhardwaj  
**System Class:** Constraint-Aware Bounded Exact Photonic Accelerator  

---

## 1. Executive Mission & Generational Strategy

The objective of **Project JANUS** is the physical realization, industrial fabrication, and commercial scale-up of the world's first **Constraint-Bounded Exact Photonic Accelerator**.

Conventional optical neural accelerators have stalled due to the **Analog Precision Collapse** (requiring an unachievable >138 dB analog SNR at scale), multi-kilowatt thermo-optic static power dissipation, nonlinear multi-wavelength interference, and amplifier noise. 

**JANUS** leapfrogs these physical limits by executing computation via **One-Hot Optical Residue Number System (RNS) spatial routing**, non-volatile **Sb2S3 dilated Beneš switching**, **1064 nm passive high-power fan-out**, and **monolithic Z-axis thermal isolation**.

### Generational Product Ladder

| Generation | Strata Count | Product Family Focus | Primary Target Models | Fabrication Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Gen-1** | 1 Stratum | Monolithic Planar MVP | Mini 16T (10×10), 32T | Lowest (Zero 3D Vias) |
| **Gen-2** | 1 & 2 Strata | Planar Edge & 3D Mini | Edge 16T (20×20), Mini 16/32 | Low (Single Int-Via) |
| **Gen-3** | 2 Strata | Dual-Stratum Scale | Mini 64T, Edge 16T, Edge 32 | Low-Medium |
| **Gen-4** | 3 Strata | 3-Stratum Edge Focus | Mini 32/64T, Edge 16/32/64 | Medium (3D Stacking) |
| **Gen-5** | 4 Strata | 4-Stratum & DC MVP | Mini 64T, Edge 32/64, DC 16 | Medium-High |
| **Gen-6** | 5 Strata | Hyperscale Flagship | DC 32T / 64T (1.01B+ sw) | Full Scale Flagship |

### Comprehensive Master Hardware & Performance Matrix (Models 1A through 6B)

All models operate under **100 GHz wave-pipelined optical cycling** (T_cycle = 10.0 ps), sustained utilization η = 0.85, and binary detection margin ≥ +4.61 dB over the Ge/Si SAC²M APD sensitivity threshold (P_sens,practical = -23.20 dBm). Laser launch power is strictly derived via the optical link budget with 2-phase 5 ps time-multiplexed steering (75% Wall-Plug Efficiency).

| Model ID | Generation & Stack Architecture | SiPh Strata | Tile Count (N_tiles) | Matrix Mesh per Tile | Total Multipliers | Total Non-Volatile Switches | Total APD Detectors | Die Area (A_die) | Master Laser (Opt / Elec) | Total System Electrical Power | Sustained INT4 Throughput | Sustained INT64 Throughput | Sustained INT4 / INT64 Efficiency | Effective Yield / Wafer (Set) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1A** | Gen-1 Monolithic Planar MVP | 1 Stratum | 16 | 32 × 32 | 16,384 | 31,457,280 (31.46M) | 4,194,304 (4.19M) | 100.00 mm² | 2.21 W / 2.95 W | **6.17 W** | 1,392.6 TMAC/s | 87.0 TMAC/s | 225.7 / 14.1 TMAC/s/W | 512 Functional / Wf |
| **1B** | Gen-1 Monolithic Planar Full | 1 Stratum | 32 | 32 × 32 | 32,768 | 62,914,560 (62.91M) | 8,388,608 (8.39M) | 200.00 mm² | 4.74 W / 6.31 W | **12.67 W** (13.03 W nom.) | 2,785.3 TMAC/s | 174.1 TMAC/s | 219.7 / 13.7 TMAC/s/W | 232 Functional / Wf |
| **2A** | Gen-2 Monolithic Planar Edge | 1 Stratum | 16 | 64 × 64 | 65,536 | 125,829,120 (125.83M) | 16,777,216 (16.78M) | 400.00 mm² | 10.15 W / 13.53 W | **23.49 W** | 5,570.6 TMAC/s | 348.2 TMAC/s | 237.1 / 14.8 TMAC/s/W | 114 Functional / Wf |
| **2B** | Gen-2 3D Mini Stack (50 mm²) | 2 Strata | 16 | 32 × 32 | 16,384 | 31,457,280 (31.46M) | 4,194,304 (4.19M) | 50.00 mm² | 2.21 W / 2.95 W | **6.17 W** | 1,392.6 TMAC/s | 87.0 TMAC/s | 225.7 / 14.1 TMAC/s/W | ≈ 512 / 3-Wafer Set |
| **2C** | Gen-2 3D Mini Stack (100 mm²)| 2 Strata | 32 | 32 × 32 | 32,768 | 62,914,560 (62.91M) | 8,388,608 (8.39M) | 100.00 mm² | 4.74 W / 6.31 W | **12.67 W** (13.03 W nom.) | 2,785.3 TMAC/s | 174.1 TMAC/s | 219.7 / 13.7 TMAC/s/W | ≈ 240 / 3-Wafer Set |
| **3A** | Gen-3 3D Mini Stack (200 mm²)| 2 Strata | 64 | 32 × 32 | 65,536 | 125,829,120 (125.83M) | 16,777,216 (16.78M) | 200.00 mm² | 10.15 W / 13.53 W | **23.49 W** | 5,570.6 TMAC/s | 348.2 TMAC/s | 237.1 / 14.8 TMAC/s/W | ≈ 116 / 3-Wafer Set |
| **3B** | Gen-3 3D Edge Stack (200 mm²)| 2 Strata | 16 | 64 × 64 | 65,536 | 125,829,120 (125.83M) | 16,777,216 (16.78M) | 200.00 mm² | 10.15 W / 13.53 W | **23.49 W** | 5,570.6 TMAC/s | 348.2 TMAC/s | 237.1 / 14.8 TMAC/s/W | ≈ 116 / 3-Wafer Set |
| **3C** | Gen-3 3D Edge Stack (400 mm²)| 2 Strata | 32 | 64 × 64 | 131,072 | 251,658,240 (251.66M) | 33,554,432 (33.55M) | 400.00 mm² | 21.75 W / 29.00 W | **45.91 W** (43.58 W nom.) | 11,141.1 TMAC/s | 696.3 TMAC/s | 242.7 / 15.2 TMAC/s/W | ≈ 57 / 3-Wafer Set |
| **4A** | Gen-4 3D Mini Stack (66.7 mm²)| 3 Strata | 32 | 32 × 32 | 32,768 | 62,914,560 (62.91M) | 8,388,608 (8.39M) | 66.67 mm² | 4.74 W / 6.31 W | **12.67 W** (13.03 W nom.) | 2,785.3 TMAC/s | 174.1 TMAC/s | 219.7 / 13.7 TMAC/s/W | ≈ 240 / 4-Wafer Set |
| **4B** | Gen-4 3D Mini Stack (133.3 mm²)| 3 Strata | 64 | 32 × 32 | 65,536 | 125,829,120 (125.83M) | 16,777,216 (16.78M) | 133.33 mm² | 10.15 W / 13.53 W | **23.49 W** | 5,570.6 TMAC/s | 348.2 TMAC/s | 237.1 / 14.8 TMAC/s/W | ≈ 116 / 4-Wafer Set |
| **4C** | Gen-4 3D Edge Stack (133.3 mm²)| 3 Strata | 16 | 64 × 64 | 65,536 | 125,829,120 (125.83M) | 16,777,216 (16.78M) | 133.33 mm² | 10.15 W / 13.53 W | **23.49 W** | 5,570.6 TMAC/s | 348.2 TMAC/s | 237.1 / 14.8 TMAC/s/W | ≈ 116 / 4-Wafer Set |
| **4D** | Gen-4 3D Edge Stack (266.7 mm²)| 3 Strata | 32 | 64 × 64 | 131,072 | 251,658,240 (251.66M) | 33,554,432 (33.55M) | 266.67 mm² | 21.75 W / 29.00 W | **45.91 W** (43.58 W nom.) | 11,141.1 TMAC/s | 696.3 TMAC/s | 242.7 / 15.2 TMAC/s/W | ≈ 57 / 4-Wafer Set |
| **4E** | Gen-4 3D Edge Flagship (533.3 mm²)| 3 Strata | 64 | 64 × 64 | 262,144 | 503,316,480 (503.32M) | 67,108,864 (67.11M) | 533.33 mm² | 46.61 W / 62.15 W | **92.97 W** | 22,282.2 TMAC/s | 1,392.6 TMAC/s | 239.7 / 15.0 TMAC/s/W | ≈ 28 / 4-Wafer Set |
| **5A** | Gen-5 3D Mini Stack (100 mm²)| 4 Strata | 64 | 32 × 32 | 65,536 | 125,829,120 (125.83M) | 16,777,216 (16.78M) | 100.00 mm² | 10.15 W / 13.53 W | **23.49 W** | 5,570.6 TMAC/s | 348.2 TMAC/s | 237.1 / 14.8 TMAC/s/W | ≈ 116 / 5-Wafer Set |
| **5B** | Gen-5 3D Edge Stack (200 mm²)| 4 Strata | 32 | 64 × 64 | 131,072 | 251,658,240 (251.66M) | 33,554,432 (33.55M) | 200.00 mm² | 21.75 W / 29.00 W | **45.91 W** (43.58 W nom.) | 11,141.1 TMAC/s | 696.3 TMAC/s | 242.7 / 15.2 TMAC/s/W | ≈ 57 / 5-Wafer Set |
| **5C** | Gen-5 3D Edge Stack (400 mm²)| 4 Strata | 64 | 64 × 64 | 262,144 | 503,316,480 (503.32M) | 67,108,864 (67.11M) | 400.00 mm² | 46.61 W / 62.15 W | **92.97 W** | 22,282.2 TMAC/s | 1,392.6 TMAC/s | 239.7 / 15.0 TMAC/s/W | ≈ 28 / 5-Wafer Set |
| **5D** | Gen-5 3D Datacenter MVP (400 mm²)| 4 Strata | 16 | 128 × 128 | 262,144 | 503,316,480 (503.32M) | 67,108,864 (67.11M) | 400.00 mm² | 46.61 W / 62.15 W | **90.39 W** | 22,282.2 TMAC/s | 1,392.6 TMAC/s | 246.5 / 15.41 TMAC/s/W | ≈ 28 / 5-Wafer Set |
| **6A** | Gen-6 3D Datacenter Master (640 mm²)| 5 Strata | 32 | 128 × 128 | 524,288 | 1,006,632,960 (1.0066B)| 134,217,728 (134.22M)| 640.00 mm² | 99.89 W / 133.19 W | **186.65 W** (186.79 W nom.)| 44,564.5 TMAC/s | 2,785.3 TMAC/s | 238.8 / 14.92 TMAC/s/W | ≈ 14 / 6-Wafer Set |
| **6B** | Gen-6 3D Hyperscale Module (1,280 mm²)| 5 Strata | 64 | 128 × 128 | 1,048,576 | 2,013,265,920 (2.013B)| 268,435,456 (268.44M)| 1,280.00 mm² | 214.08 W / 285.44 W| **392.36 W** | 89,129.0 TMAC/s | 5,570.6 TMAC/s | 227.2 / 14.20 TMAC/s/W | ≈ 7 / 6-Wafer Set |

---

## Product Positioning & Customer Perspective: Edge 16-Tile vs. Mini 64-Tile

A common architectural question arises when evaluating the **Edge 16-Tile** and the **Mini 64-Tile** models. Both feature exactly **65,536 optical multipliers**, consume **23.49 W** of power, and occupy identical silicon area in their respective stacked generations (200.00 mm² in Gen-3 dual-stratum, 133.33 mm² in Gen-4 3-stratum, and 100.00 mm² in Gen-5 4-stratum). However, they serve completely divergent customer profiles:

### The Mini 64-Tile (32 × 32 per tile)
* **Customer Profile:** Robotics, Autonomous Vehicles (AV), and multi-sensor IoT edge nodes.
* **Workload Dynamics:** Requires executing many smaller, independent neural networks simultaneously. For example, an AV might need to process 8 radar streams, 4 lidar feeds, and 12 camera feeds at once.
* **Advantage:** The 64 independent tiles allow the OS scheduler to achieve **massive multi-tenancy**. The customer can map 64 independent 32 × 32 matrix workloads in parallel without them blocking each other, achieving true spatial multitasking.

### The Edge 16-Tile (64 × 64 per tile)
* **Customer Profile:** Local LLM Inference (e.g., LLaMA-3 8B), on-premise generative AI, and heavy monolithic signal processing.
* **Workload Dynamics:** Requires executing singular, massive dense matrix multiplications (GEMMs). 
* **Advantage:** The 64 × 64 matrix dimension allows for **4x larger contiguous matrix multiplications** per cycle per tile. This drastically reduces the software compiler overhead and memory-fetch bottlenecks associated with slicing massive LLM weight matrices into tiny 32 × 32 blocks. 

---

## 2. Generation 1: Single-Stratum Monolithic Architecture (Gen-1)

Generation 1 is the **Alpha Minimum Viable Product (MVP)** family. By consolidating all optical routing, input modulators, splitting trees, and photodetectors into a **single monolithic SiPh stratum** over an ultra-thick 250 µm SiO₂ thermal buffer, Gen-1 eliminates the need for interlayer vertical optical grating couplers and wafer-to-wafer 3D optical alignment.

> [!NOTE]
> **Thermal Diffusion Physics Note:** The monolithic planar Gen-1 architecture employs an ultra-thick 250 µm SiO₂ buffer layer designed for maximum thermal isolation during initial single-stratum packaging (α = 9.05 × 10⁻⁷ m²/s, τ_diff = (250 µm)² / α = 69.06 ms = 13,812 JIR cycles). In contrast, the paper's highly compact multi-stratum reference package uses a 100 µm primary SiO₂ buffer (τ_diff = (100 µm)² / α = 11.05 ms = 2,210 JIR cycles). Both satisfy the fundamental JANUS design rule τ_diff ≫ τ_JIR = 5 µs by over three orders of magnitude.

### Monolithic 3-Layer Physical Stack

```
==================================================================================
  LAYER 2: MONOLITHIC SiPh CORE & DETECTOR STRATUM (30 µm)
  - LiTaO3 1x256 Pockels Input Modulator Trees (50 aJ/switch @ 100 GHz)
  - Passive Single-Wavelength 1064 nm MMI Splitting H-Tree Bus
  - Non-Volatile Dilated PCM Beneš Routing Fabrics (Sb2S3 Graphene Micro-Heater, 0 W Static Hold)
  - Monolithic Ge/Si SAC²M Avalanche Photodetector Array (1.00 - 1.10 µm² unit pixel)
----------------------------------------------------------------------------------
  LAYER 1.5: ULTRA-THICK MONOLITHIC SiO2 THERMAL BUFFER (250 µm)
  - Thermal Diffusivity: α = 9.05 × 10⁻⁷ m²/s | Thermal Diffusion Time: τ_diff = 69.06 ms (13,812 JIR cycles)
  - High-Aspect-Ratio Vertical Cu Through-Dielectric Vias (TDVs) for Electrical I/O
----------------------------------------------------------------------------------
  LAYER 1: CMOS BASE LOGIC, CRT ENGINE & READOUT SUBSTRATE (50 µm)
  - Event-Driven StrongARM Regenerative Latches & S/H Column Multiplexing (~100 aJ / detection)
  - High-Speed RNS Modulo Decomposition Front-End (x_i = X mod m_i, m_i <= 256)
  - Pipelined CRT Reconstruction Adder Tree (t_CRT ~ 210 ps) & JIR Consistency Checker
  - JIR Real-Time Thermal Trend Tracking & Predictive RRNS Failover Engine
==================================================================================
  TOTAL BARE-DIE MONOLITHIC THICKNESS: 50 µm + 250 µm + 30 µm = 330 µm (0.33 mm)
==================================================================================
```

### Hybrid Memory-Optical PRNS & 3-Equation 64-Bit Decomposition Engine
To eliminate dynamic range overflow and precision collapse in 64-bit integer matrix multiplications without increasing waveguide count beyond 256 or altering 15-stage Beneš network symmetry, JANUS employs a **Hybrid Memory-Optical PRNS** architecture governed by **Hybrid Partitioning** (Optics exclusively performs $1 \times 1$ element-wise multiplications, while accumulation occurs in CMOS).

* **32-Bit Word Decomposition:** Operands $X, Y \in [0, 2^{64}-1]$ are split into 32-bit halves: $X = X_H \cdot 2^{32} + X_L, Y = Y_H \cdot 2^{32} + Y_L$.
* **Three-Equation Formulation:** Matrix multiplication decomposes into three distinct operations:
  1. **Equation 1 ($X_L \cdot Y_L$):** Computed fully optically in **Cluster 0** (8 tiles, $\mathcal{M}_8$).
  2. **Equation 2 ($X_H \cdot Y_H$):** Computed fully optically in **Cluster 1** (8 tiles, $\mathcal{M}_8$).
  3. **Equation 3 ($X_L Y_H + X_H Y_L$):** The massive cross-term is offloaded out of the optics entirely and computed in CMOS via **The Memory Trick** using ultra-fast SRAM Lookup Tables (LUTs).
* **8-Modulus Optical PRNS Set:** Uses the verified 8-modulus set $\mathcal{M}_8 = \{255, 253, 251, 247, 241, 239, 233, 229\}$ verified via Z3 SMT solver ($M_8 \approx 5.68 \times 10^{19} > 2^{62}$), completely stripping the 9th optical modulus (227) and eradicating modular overflow.
* **CMOS Reconstruction & Accumulation:** CMOS readout reconstructs the optical sub-products via 8-channel CRT and performs final shift-and-add accumulation in an 80-bit carry-save adder tree.
* **Throughput Scaling:**
  * **Model 1A (16 tiles):** 1 full INT64 GEMM in **1 single 10 ps cycle** (**87.0 TMAC/s sustained**).
  * **Model 1B (32 tiles):** 2 parallel INT64 GEMMs (**174.1 TMAC/s sustained**).
  * **64-Tile Models (3A, 4B, etc.):** 4 parallel INT64 GEMMs (**348.2 TMAC/s sustained**).
### Dual-Tier Thermal Specifications & Material Retention Hierarchy
To ensure absolute reliability across both active 100 GHz wave-pipelined silicon computing and long-term non-volatile weight retention, JANUS enforces a strict **Dual-Tier Thermal Operating Boundary**:

```
[ Ambient Reference: 25°C ] 
       │
       ▼  (Normal Steady-State SiPh Rise: ΔT_ss ≈ +0.21 K to +0.35 K)
[ Nominal Commercial Ceiling: Top,nominal = 70.0°C ]
  - Standard Commercial IC rating (0°C to 70°C).
  - JIR Real-Time Thermal Scheduler preemptively triggers rotation at 0.9 × Top = 63.0°C.
  - Maintains <1.8 µA TIA noise, <1 nA APD dark current, and 100 GHz StrongARM timing.
       │
       ▼  (Worst-Case Fan Failure / Thermal Throttle Buffer: +30°C Margin)
[ Hard Physical Retention Limit: Tretention,max = 100.0°C ]
  - Guaranteed 10-Year Non-Volatile Data Retention Gate for Sb2S3 Phase-Change Switches.
  - Arrhenius activation energy barrier (E_a = 2.45 eV) prevents spontaneous crystallization drift.
  - Hard JIR Emergency Fail-Safe: laser power cut if die temp breaches 100°C.
       │
       ▼  (+50°C Physical Safety Margin)
[ Crystallization Onset Barrier: Tcryst,guard = 150.0°C ]
  - Physical amorphous-to-crystalline phase transition onset.
```

---

### Model 1A: JANUS Mini 16-Tile (Standardized 10 mm × 10 mm)

Model 1A is the primary silicon tapeout vehicle: a compact 100 mm² monolithic accelerator operating at 100 GHz.

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 16 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Multiplier Count per Tile:** 32² = 1,024 optical multipliers
* **Total Multipliers on Die:** 16 × 1,024 = **16,384 multipliers**
* **Waveguide Alphabet per Multiplier:** 256 waveguides (One-Hot 8-bit residue representation)
* **Total Spatial Waveguide Channels:** 16,384 × 256 = **4,194,304 channels**
* **Beneš Routing Stages (S):** 2·log₂(256) - 1 = **15 stages** (universal)
* **Switches per Multiplier Fabric:** (256/2) × 15 = 128 × 15 = **1,920 switches**
* **Total Non-Volatile Sb2S3 Switches:** 16,384 × 1,920 = **31,457,280 switches** (≈ 31.46 Million)
* **Terminal Ge/Si SAC²M APD Pixels:** 16,384 × 256 = **4,194,304 detectors** (≈ 4.19 Million)
* **Active Detectors per 10 ps Cycle:** 16,384 active events (1-in-256 spatial sparsity; 8,192 illuminated per 5 ps phase)

#### 2. Physical Layout & Area Budget (10.0 mm × 10.0 mm)

| Functional Component Block | Unit Dimension | Physical Area (mm²) |
| :--- | :--- | :--- |
| **1. Non-Volatile PCM Switch Cells (31.46M units)** | 1.35 µm² (relaxed) | 42.47 mm² |
| **2. In-Plane Routing Shuffles & Crossing Matrices** | Low-crosstalk MMI | 20.20 mm² |
| **3. Active 1×256 LiTaO₃ Input Routers (16,384 units)** | 1.15 mm² / router | 18.84 mm² |
| **4. Master Laser 1:8,192 MMI Distribution H-Tree** | Low-loss 13 stages | 4.50 mm² |
| **5. Monolithic Ge/Si SAC²M APDs (4.19M pixels)** | 1.00 – 1.10 µm² | 4.40 mm² |
| **6. Scribe Lines, Cu Perimeter Shunt, I/O & Dicing** | 15.5% Margin | 15.59 mm² |
| **TOTAL STANDARDIZED DIE FOOTPRINT (A_die)** | **10.0 mm × 10.0 mm** | **100.00 mm²** |

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (13 stages of 1:2 MMIs for 8,192 branches):** L_split,ideal = 10·log₁₀(2¹³) = **39.13 dB**
* **Excess Component Loss (L_excess):** 13 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Prop/Cpl) = **12.90 dB**
* **Total Optical Distribution Loss (L_total):** 39.13 dB + 12.90 dB = **52.03 dB**
* **Delivered Receiver Power (P_det):** **-18.59 dBm** (13.84 µW)
* **Receiver Practical Sensitivity (P_sens):** **-23.20 dBm** (4.79 µW @ BER = 10⁻¹⁸)
* **Net Binary Detection Margin:** (-18.59 dBm) - (-23.20 dBm) = **+4.61 dB** (Zero In-Line Amplifiers)
* **Master Laser Optical Power (P_laser,opt):** **2.21 W Optical CW** (+33.44 dBm, exact link budget)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **2.95 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 2.21 W Optical):** 2.95 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 0.51 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 0.16 W
* **Optical Amplification (SOAs/EDFAs):** 0.00 W (Eliminated)
* **PCM Routing Switches (Static Hold):** 0.00 W (Non-Volatile)
* **CMOS Encoders, CRT Adder Trees & Adders:** 1.05 W
* **JIR Scheduler & Thermal Management Engine:** 1.50 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **6.17 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 6.17 W / 100 mm² = **0.0617 W/mm²** (6.17 W/cm²)
* **SiO₂ Buffer Heat Capacity (C_SiO₂):** **38.67 mJ/K** (55.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR computation cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (6.17 W × 5 µs) / 38.67 mJ/K = **0.00080°C** = **0.80 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 225.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 112.8 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 56.4 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 204.8 TMAC/s | 174.1 TMAC/s | 28.2 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 102.4 TMAC/s | 87.0 TMAC/s | 14.1 TMAC/s/W |

#### 7. Foundry Wafer Yield (300 mm Silicon Line)
* **Gross Dies per Wafer (DPW):** **640 Raw Dies / Wafer**
* **Net Usable Good Dies (@ 80% line yield):** **512 Functional Accelerators / Wafer**

---

### Model 1B: JANUS Mini 32-Tile (Full-Capacity 200 mm²)

Model 1B doubles the parallel tile count to 32 tiles on a monolithic 200 mm² die, unlocking native 64-bit integer execution across all 16 CRT channels simultaneously with 2-way tile redundancy.

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Multiplier Count per Tile:** 32² = 1,024 optical multipliers
* **Total Multipliers on Die:** 32 × 1,024 = **32,768 multipliers**
* **Total Spatial Waveguide Channels:** 32,768 × 256 = **8,388,608 channels**
* **Total Non-Volatile Sb2S3 Switches:** 32,768 × 1,920 = **62,914,560 switches** (≈ 62.91 Million)
* **Terminal Ge/Si SAC²M APD Pixels:** 32,768 × 256 = **8,388,608 detectors** (≈ 8.39 Million)

#### 2. Physical Layout & Area Budget (14.14 mm × 14.14 mm)
* **Die Area (A_die):** **200.00 mm²** (14.14 mm × 14.14 mm × 0.33 mm)
* **Switch Core Footprint:** 78.64–84.93 mm²
* **Routing Shuffles & Crossing Matrices:** 40.40 mm²
* **Active LiTaO₃ Routers (32,768 units):** 37.68 mm²
* **Passive MMI H-Tree Distribution:** 8.80 mm²
* **Monolithic Ge/Si APD Array (8.39M pixels):** 8.80 mm²
* **Scribe Lines, Cu Perimeter Shunt, I/O & Dicing:** 19.39 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (14 stages of 1:2 MMIs for 16,384 branches):** L_split,ideal = 10·log₁₀(2¹⁴) = **42.14 dB**
* **Excess Path Loss (L_excess):** 14 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Prop/Cpl) = **13.20 dB**
* **Total Optical Distribution Loss (L_total):** 42.14 dB + 13.20 dB = **55.34 dB**
* **Target Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **4.74 W Optical CW** (+36.75 dBm, Table XV nominal ≈ 5.0 W)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **6.31 Watts** (nominal 6.67 W)

#### 4. Full-System Electrical Power Breakdown (From Table XV of main.tex)
* **1064 nm Master Laser (75% WPE, 4.74 W Optical):** 6.31 W (nominal 6.67 W)
* **LiTaO₃ Pockels Input Routers (100 GHz):** 1.02 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 0.33 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 2.01 W
* **JIR Scheduler & Thermal Management Engine:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **12.67 Watts** (nominal Table XV baseline: **13.03 Watts**)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 12.67 W / 200 mm² = **0.0634 W/mm²** (6.34 W/cm²)
* **SiO₂ Buffer Heat Capacity (C_SiO₂):** **77.33 mJ/K** (110.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (12.67 W × 5 µs) / 77.33 mJ/K = **0.00082°C** = **0.82 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 219.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 109.9 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 54.9 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 27.5 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 204.8 TMAC/s | 174.1 TMAC/s | 13.7 TMAC/s/W |

#### 7. Foundry Wafer Yield (300 mm Silicon Line)
* **Gross Dies per Wafer (DPW):** **290 Raw Dies / Wafer**
* **Net Usable Good Dies (@ 80% line yield):** **232 Functional Accelerators / Wafer**

---

## 3. Generation 2: Dual-Stratum 3D Heterogeneous Architecture & Planar Edge (Gen-2)

Generation 2 introduces two critical evolutionary paths:
1. **Model 2A (16-Tile Planar Edge):** Scaling the matrix mesh from 32 × 32 to 64 × 64 (4,096 multipliers/tile) in a monolithic single stratum (400 mm²).
2. **Models 2B and 2C (2-Stratum 3D Mini):** Introducing **2-Stratum vertical SiPh stacking** separated by a 50 µm inter-stratum SiO₂ thermal buffer, cutting die footprint by 50%.

### Dual-Stratum 5-Layer Physical Stack Architecture

```
==================================================================================
  LAYER 4: SiPh STRATUM 2 (30 µm)
  - Dilated Beneš Routing Stages 8-15 (Sb2S3 Switches, 0 W Static Hold)
  - Monolithic Ge/Si SAC²M APD Array (4.19M - 8.39M pixels)
----------------------------------------------------------------------------------
  LAYER 3.5: INTER-STRATUM SiO2 THERMAL BUFFER (50 µm)
  - Low-Loss Vertical Optical Grating Couplers / 3D Waveguide Vias (< 0.40 dB / via)
  - Thermal Diffusivity: α = 9.05 × 10⁻⁷ m²/s | Inter-stratum diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 3: SiPh STRATUM 1 (30 µm)
  - LiTaO3 1x256 Pockels Input Modulators (50 aJ/switch @ 100 GHz)
  - Passive 1064 nm MMI Splitting Tree & Beneš Routing Stages 1-7
----------------------------------------------------------------------------------
  LAYER 2: MONOLITHIC PRIMARY SiO2 THERMAL BUFFER (250 µm)
  - Thermal Diffusion Time: τ_diff = 69.06 ms (13,812 JIR cycles)
  - High-Aspect-Ratio Vertical Cu Through-Dielectric Vias (TDVs)
----------------------------------------------------------------------------------
  LAYER 1: CMOS BASE LOGIC & CRT RECONSTRUCTION SUBSTRATE (50 µm)
  - StrongARM Regenerative Latches, RNS Encoders & Pipelined CRT Engine
==================================================================================
  TOTAL BARE-DIE ACTIVE 3D STACK HEIGHT: 50 + 250 + 30 + 50 + 30 = 410 µm (0.41 mm)
==================================================================================
```

---

### Model 2A: JANUS Edge 16-Tile (Planar Monolithic 400 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 16 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 16 × 4,096 = **65,536 multipliers**
* **Waveguide Alphabet per Multiplier:** 256 waveguides (One-Hot 8-bit residue representation)
* **Total Spatial Waveguide Channels:** 65,536 × 256 = **16,777,216 channels** (≈ 16.78 Million)
* **Beneš Routing Stages (S):** 2·log₂(256) - 1 = **15 stages**
* **Switches per Multiplier Fabric:** (256/2) × 15 = 128 × 15 = **1,920 switches**
* **Total Non-Volatile Sb2S3 Switches:** 65,536 × 1,920 = **125,829,120 switches** (≈ 125.83 Million)
* **Terminal Ge/Si SAC²M APD Pixels:** 65,536 × 256 = **16,777,216 detectors** (≈ 16.78 Million)
* **Active Detectors per 10 ps Cycle:** 65,536 active events (32,768 illuminated per 5 ps phase)

#### 2. Physical Layout & Area Budget (20.0 mm × 20.0 mm)
* **Die Footprint (A_die):** **400.00 mm²** (20.0 mm × 20.0 mm × 0.33 mm)
* **Switch Core Footprint:** 169.87 mm²
* **Routing Shuffles & Crossing Matrices:** 80.80 mm²
* **Active LiTaO₃ Routers (65,536 units):** 75.37 mm²
* **Passive MMI H-Tree Distribution:** 17.50 mm²
* **Monolithic Ge/Si APD Array (16.78M pixels):** 17.62 mm²
* **Scribe Lines, Cu Perimeter Shunt, I/O & Dicing:** 38.84 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (15 stages of 1:2 MMIs for 32,768 branches):** L_split,ideal = 10·log₁₀(2¹⁵) = **45.15 dB**
* **Excess Path Loss (L_excess):** 15 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Prop/Cpl) = **13.50 dB**
* **Total Optical Distribution Loss (L_total):** 45.15 dB + 13.50 dB = **58.65 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **10.15 W Optical CW** (+40.06 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **13.53 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 10.15 W Optical):** 13.53 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 2.05 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 0.66 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 4.25 W
* **JIR Scheduler & Thermal Management Engine:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **23.49 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 23.49 W / 400 mm² = **0.0587 W/mm²** (5.87 W/cm²)
* **SiO₂ Buffer Heat Capacity (C_SiO₂):** **154.66 mJ/K** (220.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (23.49 W × 5 µs) / 0.15466 J/K = **0.00076°C** = **0.76 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 237.1 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 118.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 59.3 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 29.6 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 14.8 TMAC/s/W |

#### 7. Foundry Wafer Yield (300 mm Silicon Line)
* **Gross Dies per Wafer (DPW):** **143 Raw Dies / Wafer**
* **Net Usable Good Dies (@ 80% line yield):** **114 Functional Accelerators / Wafer**

---

### Model 2B: JANUS Mini 16-Tile (2-Stratum 3D Stack 50.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 16 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Total Multipliers on Die:** 16 × 1,024 = **16,384 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **31,457,280 switches** (15.73M per stratum)
* **Terminal Ge/Si APD Pixels:** **4,194,304 detectors** on Stratum 2
* **SiPh Strata Count:** 2 Strata (30 µm each) + 50 µm Inter-Stratum SiO₂ Buffer

#### 2. Physical Layout & Area Budget (7.07 mm × 7.07 mm)
* **Die Footprint (A_die):** **50.00 mm²** (7.07 mm × 7.07 mm × 0.41 mm)
* **Switch Footprint per Stratum:** 21.24 mm²
* **Routing Shuffles & Interlayer Vias:** 10.50 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 9.42 mm²
* **Passive MMI H-Tree & APD Array:** 4.40 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 4.44 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (13 stages of 1:2 MMIs):** L_split,ideal = **39.13 dB**
* **Excess Path Loss (L_excess):** 13 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 0.80 dB (Interlayer) + 0.70 dB (Prop/Cpl) = **12.90 dB**
* **Total Optical Distribution Loss (L_total):** 39.13 dB + 12.90 dB = **52.03 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **2.21 W Optical CW** (+33.44 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **2.95 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 2.21 W Optical):** 2.95 W
* **LiTaO₃ Pockels Input Routers + APD Readout:** 0.67 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 2.55 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **6.17 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 6.17 W / 50.0 mm² = **0.1234 W/mm²** (12.34 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **19.33 mJ/K** (27.5 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Inter-Stratum SiO₂ Buffer (50 µm):** τ_diff,inter = **2.76 ms** = **552 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (6.17 W × 5 µs) / 0.01933 J/K = **0.00160°C** = **1.60 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 225.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 112.8 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 56.4 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 204.8 TMAC/s | 174.1 TMAC/s | 28.2 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 102.4 TMAC/s | 87.0 TMAC/s | 14.1 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 50.00 mm² (7.07 mm × 7.07 mm)
* **Wafer Set Consumption:** 3 wafers per run (1 CMOS base + 2 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 512 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 3-wafer stack).

---

### Model 2C: JANUS Mini 32-Tile (2-Stratum 3D Stack 100.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Total Multipliers on Die:** 32 × 1,024 = **32,768 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **62,914,560 switches** (31.46M per stratum)
* **Terminal Ge/Si APD Pixels:** **8,388,608 detectors** on Stratum 2
* **SiPh Strata Count:** 2 Strata (30 µm each) + 50 µm Inter-Stratum SiO₂ Buffer

#### 2. Physical Layout & Area Budget (10.0 mm × 10.0 mm)
* **Die Footprint (A_die):** **100.00 mm²** (10.0 mm × 10.0 mm × 0.41 mm)
* **Switch Footprint per Stratum:** 42.47 mm²
* **Routing Shuffles & Interlayer Vias:** 21.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 18.84 mm²
* **Passive MMI H-Tree & APD Array:** 8.80 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 8.89 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (14 stages of 1:2 MMIs):** L_split,ideal = **42.14 dB**
* **Excess Path Loss (L_excess):** 14 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 0.80 dB (Interlayer) + 0.70 dB (Prop/Cpl) = **13.20 dB**
* **Total Optical Distribution Loss (L_total):** 42.14 dB + 13.20 dB = **55.34 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **4.74 W Optical CW** (+36.75 dBm, Table XV nominal ≈ 5.0 W)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **6.31 Watts** (nominal 6.67 W)

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 4.74 W Optical):** 6.31 W (nominal 6.67 W)
* **LiTaO₃ Pockels Input Routers + APD Readout:** 1.35 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 5.01 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **12.67 Watts** (nominal Table XV baseline: **13.03 Watts**)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 12.67 W / 100.0 mm² = **0.1267 W/mm²** (12.67 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **38.67 mJ/K** (55.0 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Inter-Stratum SiO₂ Buffer (50 µm):** τ_diff,inter = **2.76 ms** = **552 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (12.67 W × 5 µs) / 0.03867 J/K = **0.00164°C** = **1.64 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 219.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 109.9 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 54.9 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 27.5 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 204.8 TMAC/s | 174.1 TMAC/s | 13.7 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 100.00 mm² (10.0 mm × 10.0 mm)
* **Wafer Set Consumption:** 3 wafers per run (1 CMOS base + 2 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 240 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 3-wafer stack).

---

## 4. Generation 3: Dual-Stratum Scale-Up & High-Density Edge Acceleration (Gen-3)

Generation 3 scales the dual-stratum 3D architecture into high-density enterprise configurations:
1. **Model 3A (64-Tile 2-Stratum Mini):** Scaling Mini tiles to 64 parallel residue domains on a 200 mm² die (14.14 mm × 14.14 mm), enabling 4-way 64-bit parallel execution.
2. **Model 3B (16-Tile 2-Stratum Edge):** Consolidating the 16-Tile Edge model from planar 400 mm² down to a compact **200 mm²** 3D dual-stratum form factor.
3. **Model 3C (32-Tile 2-Stratum Edge):** A high-throughput dual-stratum edge supercomputer core packing 131,072 optical multipliers into a 400 mm² die (20.0 mm × 20.0 mm).

> [!IMPORTANT]
> **Interleaved Two-Layer Ge/Si APD Detector Block Integration:** Starting in Gen-3 for 32-tile and 64-tile models, the photodetector array is structured as a dedicated **10 µm Interleaved Two-Layer Ge/Si SAC²M APD Detector Block** (2 × 5 µm sub-arrays). This interleaved topology halves the vertical interconnect wiring pitch, suppresses inter-channel capacitive crosstalk, and establishes a uniform heat-spreading boundary directly beneath the primary heat spreader (HS1).

---

### Model 3A: JANUS Mini 64-Tile (2-Stratum 3D Stack 200.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 64 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Multiplier Count per Tile:** 32² = 1,024 optical multipliers
* **Total Multipliers on Die:** 64 × 1,024 = **65,536 multipliers**
* **Waveguide Alphabet per Multiplier:** 256 waveguides (One-Hot 8-bit residue representation)
* **Total Spatial Waveguide Channels:** 65,536 × 256 = **16,777,216 channels** (≈ 16.78 Million)
* **Beneš Routing Stages (S):** 2·log₂(256) - 1 = **15 stages**
* **Switches per Multiplier Fabric:** (256/2) × 15 = 128 × 15 = **1,920 switches**
* **Total Non-Volatile Sb2S3 Switches:** 65,536 × 1,920 = **125,829,120 switches** (≈ 125.83 Million, 62.91M per stratum)
* **Terminal Ge/Si SAC²M APD Pixels:** 65,536 × 256 = **16,777,216 detectors** on dedicated 10 µm 2-layer detector block
* **Active Detectors per 10 ps Cycle:** 65,536 active events (32,768 illuminated per 5 ps phase)
* **SiPh Strata Count:** 2 Strata (30 µm each) + 50 µm Inter-Stratum SiO₂ Buffer + 10 µm APD Block

#### 2. Physical Layout & Area Budget (14.14 mm × 14.14 mm)
* **Die Footprint (A_die):** **200.00 mm²** (14.14 mm × 14.14 mm × 0.42 mm)
* **Switch Core Footprint per Stratum:** 84.93 mm²
* **Routing Shuffles & Interlayer Vias:** 41.50 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 37.68 mm²
* **Passive MMI H-Tree & APD Array:** 17.60 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 18.29 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (15 stages of 1:2 MMIs for 32,768 branches):** L_split,ideal = **45.15 dB**
* **Excess Path Loss (L_excess):** 15 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 0.80 dB (Interlayer) + 0.70 dB (Prop/Cpl) = **13.50 dB**
* **Total Optical Distribution Loss (L_total):** 45.15 dB + 13.50 dB = **58.65 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **10.15 W Optical CW** (+40.06 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **13.53 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 10.15 W Optical):** 13.53 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 2.05 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 0.66 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 4.25 W
* **JIR Scheduler & Thermal Management Engine:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **23.49 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 23.49 W / 200.0 mm² = **0.1175 W/mm²** (11.75 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **77.33 mJ/K** (110.0 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Inter-Stratum SiO₂ Buffer (50 µm):** τ_diff,inter = **2.76 ms** = **552 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (23.49 W × 5 µs) / 0.07733 J/K = **0.00152°C** = **1.52 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 237.1 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 118.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 59.3 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 29.6 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 14.8 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 200.00 mm² (14.14 mm × 14.14 mm)
* **Wafer Set Consumption:** 3 wafers per run (1 CMOS base + 2 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 116 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 3-wafer stack).

---

### Model 3B: JANUS Edge 16-Tile (2-Stratum 3D Stack 200.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 16 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 16 × 4,096 = **65,536 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **125,829,120 switches** (62.91M per stratum)
* **Terminal Ge/Si APD Pixels:** **16,777,216 detectors** on Stratum 2
* **SiPh Strata Count:** 2 Strata (30 µm each) + 50 µm Inter-Stratum SiO₂ Buffer

#### 2. Physical Layout & Area Budget (14.14 mm × 14.14 mm)
* **Die Footprint (A_die):** **200.00 mm²** (14.14 mm × 14.14 mm × 0.41 mm)
* **Switch Footprint per Stratum:** 84.93 mm²
* **Routing Shuffles & Interlayer Vias:** 41.50 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 37.68 mm²
* **Passive MMI H-Tree & APD Array:** 17.60 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 18.29 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (15 stages of 1:2 MMIs):** L_split,ideal = **45.15 dB**
* **Excess Path Loss (L_excess):** 15 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 0.80 dB (Interlayer) + 0.70 dB (Prop/Cpl) = **13.50 dB**
* **Total Optical Distribution Loss (L_total):** 45.15 dB + 13.50 dB = **58.65 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **10.15 W Optical CW** (+40.06 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **13.53 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 10.15 W Optical):** 13.53 W
* **LiTaO₃ Pockels Input Routers + APD Readout:** 2.71 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 7.25 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **23.49 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 23.49 W / 200.0 mm² = **0.1175 W/mm²** (11.75 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **77.33 mJ/K** (110.0 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Inter-Stratum SiO₂ Buffer (50 µm):** τ_diff,inter = **2.76 ms** = **552 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (23.49 W × 5 µs) / 0.07733 J/K = **0.00152°C** = **1.52 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 237.1 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 118.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 59.3 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 29.6 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 14.8 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 200.00 mm² (14.14 mm × 14.14 mm)
* **Wafer Set Consumption:** 3 wafers per run (1 CMOS base + 2 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 116 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 3-wafer stack).

---

### Model 3C: JANUS Edge 32-Tile (2-Stratum 3D Stack 400.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 32 × 4,096 = **131,072 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **251,658,240 switches** (125.83M per stratum)
* **Terminal Ge/Si APD Pixels:** **33,554,432 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 2 Strata (30 µm each) + 50 µm Inter-Stratum SiO₂ Buffer + 10 µm APD Block

#### 2. Physical Layout & Area Budget (20.0 mm × 20.0 mm)
* **Die Footprint (A_die):** **400.00 mm²** (20.0 mm × 20.0 mm × 0.42 mm)
* **Switch Footprint per Stratum:** 169.87 mm²
* **Routing Shuffles & Interlayer Vias:** 81.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 75.37 mm²
* **Passive MMI H-Tree & APD Array:** 35.12 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 38.64 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (16 stages of 1:2 MMIs for 65,536 branches):** L_split,ideal = **48.16 dB**
* **Excess Path Loss (L_excess):** 16 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 0.80 dB (Interlayer) + 0.70 dB (Prop/Cpl) = **13.80 dB**
* **Total Optical Distribution Loss (L_total):** 48.16 dB + 13.80 dB = **61.96 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **21.75 W Optical CW** (+43.37 dBm, Table XV nominal ≈ 20.0 W)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **29.00 Watts** (nominal 26.67 W)

#### 4. Full-System Electrical Power Breakdown (From Table XV of main.tex)
* **1064 nm Master Laser (75% WPE, 21.75 W Optical):** 29.00 W (nominal 26.67 W)
* **LiTaO₃ Pockels Input Routers (100 GHz):** 4.10 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 1.31 W
* **Optical Amplification Layer:** 0.00 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 8.50 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **45.91 Watts** (nominal Table XV baseline: **43.58 Watts**, operating band 43.6–55.0 W)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 45.91 W / 400.0 mm² = **0.1148 W/mm²** (11.48 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **154.66 mJ/K** (220.0 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Inter-Stratum SiO₂ Buffer (50 µm):** τ_diff,inter = **2.76 ms** = **552 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (45.91 W × 5 µs) / 0.15466 J/K = **0.00148°C** = **1.48 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 242.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 121.3 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 60.7 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 30.3 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 15.2 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 400.00 mm² (20.0 mm × 20.0 mm)
* **Wafer Set Consumption:** 3 wafers per run (1 CMOS base + 2 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 57 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 3-wafer stack).

---

## 5. Generation 4: 3-Stratum 3D Heterogeneous Silicon Photonics (Gen-4)

Generation 4 expands vertical stacking to **3 Silicon Photonic Strata**, achieving extreme areal density across Mini and Edge product tiers, and introduces the **Edge 64-Tile Flagship (Model 4E)**.

### 3-Stratum 7-Layer Monolithic Stack Architecture

```
==================================================================================
  TOP: INTERLEAVED TWO-LAYER Ge/Si SAC²M APD DETECTOR BLOCK (10 µm)
  - 2 Vertically Stacked Ge/Si Sub-Arrays (2 × 5 µm) Handling Alternating Odd/Even Waveguide Channels
  - Dedicated Metal Routing Layers (Halved Pitch, Zero Crosstalk, Direct Contact to HS1)
==================================================================================
  LAYER 6: SiPh STRATUM 3 (30 µm)
  - Dilated Beneš Routing Stages 11-15 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 5.5: INTER-STRATUM SiO2 BUFFER 2 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 5: SiPh STRATUM 2 (30 µm)
  - Dilated Beneš Routing Stages 6-10 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 4.5: INTER-STRATUM SiO2 BUFFER 1 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 4: SiPh STRATUM 1 (30 µm)
  - LiTaO3 1x256 Pockels Input Modulators (50 aJ/switch @ 100 GHz)
  - Passive 1064 nm MMI Splitting Tree & Beneš Routing Stages 1-5
----------------------------------------------------------------------------------
  LAYER 2: MONOLITHIC PRIMARY SiO2 THERMAL BUFFER (250 µm)
  - Thermal Diffusivity: α = 9.05 × 10⁻⁷ m²/s | Thermal Diffusion Time: τ_diff = 69.06 ms (13,812 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 1: CMOS BASE LOGIC & CRT RECONSTRUCTION SUBSTRATE (50 µm)
  - StrongARM Regenerative Latches, RNS Encoders & Pipelined CRT Engine
==================================================================================
  TOTAL BARE-DIE ACTIVE 3D STACK HEIGHT: 50 + 250 + 3×30 + 2×50 + 10 = 500 µm (0.50 mm)
==================================================================================
```

---

### Model 4A: JANUS Mini 32-Tile (3-Stratum 3D Stack 66.67 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Multiplier Count per Tile:** 32² = 1,024 optical multipliers
* **Total Multipliers on Die:** 32 × 1,024 = **32,768 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **62,914,560 switches** (≈ 20.97M per stratum)
* **Terminal Ge/Si APD Pixels:** **8,388,608 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 3 Strata (30 µm each) + Two 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (8.16 mm × 8.16 mm)
* **Die Footprint (A_die):** **66.67 mm²** (8.16 mm × 8.16 mm × 0.50 mm)
* **Switch Footprint per Stratum:** 28.31 mm²
* **Routing Shuffles & Interlayer Vias:** 14.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 12.56 mm²
* **Passive MMI H-Tree & APD Array:** 5.87 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 5.93 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (14 stages of 1:2 MMIs):** L_split,ideal = **42.14 dB**
* **Excess Path Loss (L_excess):** 14 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.40 dB (Interlayer/Prop) = **13.20 dB**
* **Total Optical Distribution Loss (L_total):** 42.14 dB + 13.20 dB = **55.34 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **4.74 W Optical CW** (+36.75 dBm, Table XV nominal ≈ 5.0 W)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **6.31 Watts** (nominal 6.67 W)

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 4.74 W Optical):** 6.31 W (nominal 6.67 W)
* **LiTaO₃ Pockels Input Routers + APD Readout:** 1.35 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 5.01 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **12.67 Watts** (nominal Table XV baseline: **13.03 Watts**)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 12.67 W / 66.67 mm² = **0.1900 W/mm²** (19.00 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **25.78 mJ/K** (36.67 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (12.67 W × 5 µs) / 0.02578 J/K = **0.00246°C** = **2.46 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 219.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 109.9 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 54.9 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 27.5 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 204.8 TMAC/s | 174.1 TMAC/s | 13.7 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 66.67 mm² (8.16 mm × 8.16 mm)
* **Wafer Set Consumption:** 4 wafers per run (1 CMOS base + 3 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 240 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 4-wafer stack).

---

### Model 4B: JANUS Mini 64-Tile (3-Stratum 3D Stack 133.33 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 64 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Multiplier Count per Tile:** 32² = 1,024 optical multipliers
* **Total Multipliers on Die:** 64 × 1,024 = **65,536 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **125,829,120 switches** (≈ 41.94M per stratum)
* **Terminal Ge/Si APD Pixels:** **16,777,216 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 3 Strata (30 µm each) + Two 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (11.55 mm × 11.55 mm)
* **Die Footprint (A_die):** **133.33 mm²** (11.55 mm × 11.55 mm × 0.50 mm)
* **Switch Footprint per Stratum:** 56.62 mm²
* **Routing Shuffles & Interlayer Vias:** 27.67 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 25.12 mm²
* **Passive MMI H-Tree & APD Array:** 11.73 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 12.19 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (15 stages of 1:2 MMIs):** L_split,ideal = **45.15 dB**
* **Excess Path Loss (L_excess):** 15 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **13.50 dB**
* **Total Optical Distribution Loss (L_total):** 45.15 dB + 13.50 dB = **58.65 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **10.15 W Optical CW** (+40.06 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **13.53 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 10.15 W Optical):** 13.53 W
* **LiTaO₃ Pockels Input Routers + APD Readout:** 2.71 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 7.25 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **23.49 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 23.49 W / 133.33 mm² = **0.1762 W/mm²** (17.62 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **51.55 mJ/K** (73.33 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (23.49 W × 5 µs) / 0.05155 J/K = **0.00228°C** = **2.28 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 237.1 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 118.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 59.3 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 29.6 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 14.8 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 133.33 mm² (11.55 mm × 11.55 mm)
* **Wafer Set Consumption:** 4 wafers per run (1 CMOS base + 3 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 116 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 4-wafer stack).

---

### Model 4C: JANUS Edge 16-Tile (3-Stratum 3D Stack 133.33 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 16 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 16 × 4,096 = **65,536 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **125,829,120 switches** (≈ 41.94M per stratum)
* **Terminal Ge/Si APD Pixels:** **16,777,216 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 3 Strata (30 µm each) + Two 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (11.55 mm × 11.55 mm)
* **Die Footprint (A_die):** **133.33 mm²** (11.55 mm × 11.55 mm × 0.50 mm)
* **Switch Footprint per Stratum:** 56.62 mm²
* **Routing Shuffles & Interlayer Vias:** 27.67 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 25.12 mm²
* **Passive MMI H-Tree & APD Array:** 11.73 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 12.19 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (15 stages of 1:2 MMIs):** L_split,ideal = **45.15 dB**
* **Excess Path Loss (L_excess):** 15 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **13.50 dB**
* **Total Optical Distribution Loss (L_total):** 45.15 dB + 13.50 dB = **58.65 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **10.15 W Optical CW** (+40.06 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **13.53 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 10.15 W Optical):** 13.53 W
* **LiTaO₃ Pockels Input Routers + APD Readout:** 2.71 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 7.25 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **23.49 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 23.49 W / 133.33 mm² = **0.1762 W/mm²** (17.62 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **51.55 mJ/K** (73.33 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (23.49 W × 5 µs) / 0.05155 J/K = **0.00228°C** = **2.28 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 237.1 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 118.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 59.3 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 29.6 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 14.8 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 133.33 mm² (11.55 mm × 11.55 mm)
* **Wafer Set Consumption:** 4 wafers per run (1 CMOS base + 3 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 116 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 4-wafer stack).

---

### Model 4D: JANUS Edge 32-Tile (3-Stratum 3D Stack 266.67 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 32 × 4,096 = **131,072 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **251,658,240 switches** (≈ 83.89M per stratum)
* **Terminal Ge/Si APD Pixels:** **33,554,432 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 3 Strata (30 µm each) + Two 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (16.33 mm × 16.33 mm)
* **Die Footprint (A_die):** **266.67 mm²** (16.33 mm × 16.33 mm × 0.50 mm)
* **Switch Footprint per Stratum:** 113.25 mm²
* **Routing Shuffles & Interlayer Vias:** 54.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 50.25 mm²
* **Passive MMI H-Tree & APD Array:** 23.41 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 25.76 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (16 stages of 1:2 MMIs):** L_split,ideal = **48.16 dB**
* **Excess Path Loss (L_excess):** 16 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **13.80 dB**
* **Total Optical Distribution Loss (L_total):** 48.16 dB + 13.80 dB = **61.96 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **21.75 W Optical CW** (+43.37 dBm, Table XV nominal ≈ 20.0 W)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **29.00 Watts** (nominal 26.67 W)

#### 4. Full-System Electrical Power Breakdown (From Table XV of main.tex)
* **1064 nm Master Laser (75% WPE, 21.75 W Optical):** 29.00 W (nominal 26.67 W)
* **LiTaO₃ Pockels Input Routers (100 GHz):** 4.10 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 1.31 W
* **Optical Amplification Layer:** 0.00 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 8.50 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **45.91 Watts** (nominal Table XV baseline: **43.58 Watts**, operating band 43.6–55.0 W)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 45.91 W / 266.67 mm² = **0.1722 W/mm²** (17.22 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **103.10 mJ/K** (146.67 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (45.91 W × 5 µs) / 0.10310 J/K = **0.00223°C** = **2.23 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 242.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 121.3 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 60.7 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 30.3 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 15.2 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 266.67 mm² (16.33 mm × 16.33 mm)
* **Wafer Set Consumption:** 4 wafers per run (1 CMOS base + 3 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 57 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 4-wafer stack).

---

### Model 4E: JANUS Edge 64-Tile (3-Stratum 3D Edge Flagship 533.33 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 64 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 64 × 4,096 = **262,144 multipliers**
* **Total Spatial Waveguide Channels:** 262,144 × 256 = **67,108,864 channels** (≈ 67.11 Million)
* **Total Non-Volatile Sb2S3 Switches:** 262,144 × 1,920 = **503,316,480 switches** (≈ 503.32 Million, ≈ 167.77M per stratum)
* **Terminal Ge/Si SAC²M APD Pixels:** 67,108,864 detectors on dedicated 10 µm 2-layer detector block
* **Active Detectors per 10 ps Cycle:** 262,144 active events (131,072 illuminated per 5 ps phase)
* **SiPh Strata Count:** 3 Strata (30 µm each) + Two 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (23.09 mm × 23.09 mm)
* **Die Footprint (A_die):** **533.33 mm²** (23.09 mm × 23.09 mm × 0.50 mm)
* **Switch Footprint per Stratum:** 226.49 mm²
* **Routing Shuffles & Interlayer Vias:** 108.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 100.50 mm²
* **Passive MMI H-Tree & APD Array:** 46.82 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 51.52 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (17 stages of 1:2 MMIs for 131,072 branches):** L_split,ideal = 10·log₁₀(2¹⁷) = **51.18 dB**
* **Excess Path Loss (L_excess):** 17 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **14.10 dB**
* **Total Optical Distribution Loss (L_total):** 51.18 dB + 14.10 dB = **65.28 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **46.61 W Optical CW** (+46.69 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **62.15 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 46.61 W Optical):** 62.15 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 8.20 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 2.62 W
* **Optical Amplification Layer:** 0.00 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 17.00 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **92.97 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 92.97 W / 533.33 mm² = **0.1743 W/mm²** (17.43 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **206.21 mJ/K** (293.33 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (92.97 W × 5 µs) / 0.20621 J/K = **0.00225°C** = **2.25 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 26,214.4 TMAC/s | 22,282.2 TMAC/s | 239.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 119.8 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 59.9 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 30.0 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 15.0 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 533.33 mm² (23.09 mm × 23.09 mm)
* **Wafer Set Consumption:** 4 wafers per run (1 CMOS base + 3 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 28 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 4-wafer stack).

---

## 6. Generation 5: 4-Stratum 3D Heterogeneous Silicon Photonics & Datacenter MVP (Gen-5)

Generation 5 scales vertical stacking to **4 Silicon Photonic Strata** and inaugurates the **Datacenter Product Line** with the **Datacenter 16-Tile MVP (Model 5D)** utilizing 128 × 128 photonic matrix meshes.

### 4-Stratum 9-Layer Monolithic Stack Architecture

```
==================================================================================
  TOP: INTERLEAVED TWO-LAYER Ge/Si SAC²M APD DETECTOR BLOCK (10 µm)
  - 2 Vertically Stacked Ge/Si Sub-Arrays (2 × 5 µm) Handling Alternating Odd/Even Waveguide Channels
  - Dedicated Metal Routing Layers (Halved Pitch, Zero Crosstalk, Direct Contact to HS1)
==================================================================================
  LAYER 8: SiPh STRATUM 4 (30 µm)
  - Dilated Beneš Routing Stages 12-15 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 7.5: INTER-STRATUM SiO2 BUFFER 3 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 7: SiPh STRATUM 3 (30 µm)
  - Dilated Beneš Routing Stages 8-11 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 6.5: INTER-STRATUM SiO2 BUFFER 2 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 6: SiPh STRATUM 2 (30 µm)
  - Dilated Beneš Routing Stages 4-7 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 5.5: INTER-STRATUM SiO2 BUFFER 1 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 5: SiPh STRATUM 1 (30 µm)
  - LiTaO3 1x256 Pockels Input Modulators (50 aJ/switch @ 100 GHz)
  - Passive 1064 nm MMI Splitting Tree & Beneš Routing Stages 1-3
----------------------------------------------------------------------------------
  LAYER 2: MONOLITHIC PRIMARY SiO2 THERMAL BUFFER (250 µm)
  - Thermal Diffusivity: α = 9.05 × 10⁻⁷ m²/s | Thermal Diffusion Time: τ_diff = 69.06 ms (13,812 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 1: CMOS BASE LOGIC & CRT RECONSTRUCTION SUBSTRATE (50 µm)
  - StrongARM Regenerative Latches, RNS Encoders & Pipelined CRT Engine
==================================================================================
  TOTAL BARE-DIE ACTIVE 3D STACK HEIGHT: 50 + 250 + 4×30 + 3×50 + 10 = 580 µm (0.58 mm)
==================================================================================
```

---

### Model 5A: JANUS Mini 64-Tile (4-Stratum 3D Stack 100.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 64 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 32 × 32 matrix mesh per tile
* **Multiplier Count per Tile:** 32² = 1,024 optical multipliers
* **Total Multipliers on Die:** 64 × 1,024 = **65,536 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **125,829,120 switches** (≈ 31.46M per stratum)
* **Terminal Ge/Si APD Pixels:** **16,777,216 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 4 Strata (30 µm each) + Three 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (10.0 mm × 10.0 mm)
* **Die Footprint (A_die):** **100.00 mm²** (10.0 mm × 10.0 mm × 0.58 mm)
* **Switch Footprint per Stratum:** 42.47 mm²
* **Routing Shuffles & Interlayer Vias:** 21.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 18.84 mm²
* **Passive MMI H-Tree & APD Array:** 8.80 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 8.89 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (15 stages of 1:2 MMIs):** L_split,ideal = **45.15 dB**
* **Excess Path Loss (L_excess):** 15 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **13.50 dB**
* **Total Optical Distribution Loss (L_total):** 45.15 dB + 13.50 dB = **58.65 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **10.15 W Optical CW** (+40.06 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **13.53 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 10.15 W Optical):** 13.53 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 2.05 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 0.66 W
* **CMOS Encoders, CRT Adder Trees & JIR Engine:** 7.25 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **23.49 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 23.49 W / 100.0 mm² = **0.2349 W/mm²** (23.49 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **38.67 mJ/K** (55.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (23.49 W × 5 µs) / 0.03867 J/K = **0.00304°C** = **3.04 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 237.1 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 118.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 59.3 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 29.6 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 409.6 TMAC/s | 348.2 TMAC/s | 14.8 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 100.00 mm² (10.0 mm × 10.0 mm)
* **Wafer Set Consumption:** 5 wafers per run (1 CMOS base + 4 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 116 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 5-wafer stack).

---

### Model 5B: JANUS Edge 32-Tile (4-Stratum 3D Stack 200.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 32 × 4,096 = **131,072 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **251,658,240 switches** (≈ 62.91M per stratum)
* **Terminal Ge/Si APD Pixels:** **33,554,432 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 4 Strata (30 µm each) + Three 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (14.14 mm × 14.14 mm)
* **Die Footprint (A_die):** **200.00 mm²** (14.14 mm × 14.14 mm × 0.58 mm)
* **Switch Footprint per Stratum:** 84.93 mm²
* **Routing Shuffles & Interlayer Vias:** 41.50 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 37.68 mm²
* **Passive MMI H-Tree & APD Array:** 17.60 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 18.29 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (16 stages of 1:2 MMIs):** L_split,ideal = **48.16 dB**
* **Excess Path Loss (L_excess):** 16 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **13.80 dB**
* **Total Optical Distribution Loss (L_total):** 48.16 dB + 13.80 dB = **61.96 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **21.75 W Optical CW** (+43.37 dBm, Table XV nominal ≈ 20.0 W)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **29.00 Watts** (nominal 26.67 W)

#### 4. Full-System Electrical Power Breakdown (From Table XV of main.tex)
* **1064 nm Master Laser (75% WPE, 21.75 W Optical):** 29.00 W (nominal 26.67 W)
* **LiTaO₃ Pockels Input Routers (100 GHz):** 4.10 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 1.31 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 8.50 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **45.91 Watts** (nominal Table XV baseline: **43.58 Watts**, operating band 43.6–55.0 W)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 45.91 W / 200.0 mm² = **0.2296 W/mm²** (22.96 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **77.33 mJ/K** (110.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (45.91 W × 5 µs) / 0.07733 J/K = **0.00297°C** = **2.97 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 242.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 121.3 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 60.7 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 30.3 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 819.2 TMAC/s | 696.3 TMAC/s | 15.2 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 200.00 mm² (14.14 mm × 14.14 mm)
* **Wafer Set Consumption:** 5 wafers per run (1 CMOS base + 4 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 57 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 5-wafer stack).

---

### Model 5C: JANUS Edge 64-Tile (4-Stratum 3D Stack 400.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 64 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 64 × 64 matrix mesh per tile
* **Multiplier Count per Tile:** 64² = 4,096 optical multipliers
* **Total Multipliers on Die:** 64 × 4,096 = **262,144 multipliers**
* **Total Non-Volatile Sb2S3 Switches:** **503,316,480 switches** (≈ 125.83M per stratum)
* **Terminal Ge/Si APD Pixels:** **67,108,864 detectors** on dedicated 10 µm 2-layer detector block
* **SiPh Strata Count:** 4 Strata (30 µm each) + Three 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (20.0 mm × 20.0 mm)
* **Die Footprint (A_die):** **400.00 mm²** (20.0 mm × 20.0 mm × 0.58 mm)
* **Switch Footprint per Stratum:** 169.87 mm²
* **Routing Shuffles & Interlayer Vias:** 81.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 75.37 mm²
* **Passive MMI H-Tree & APD Array:** 35.12 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 38.64 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (17 stages of 1:2 MMIs):** L_split,ideal = **51.18 dB**
* **Excess Path Loss (L_excess):** 17 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **14.10 dB**
* **Total Optical Distribution Loss (L_total):** 51.18 dB + 14.10 dB = **65.28 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **46.61 W Optical CW** (+46.69 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **62.15 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 46.61 W Optical):** 62.15 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 8.20 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 2.62 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 17.00 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **92.97 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 92.97 W / 400.0 mm² = **0.2324 W/mm²** (23.24 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **154.66 mJ/K** (220.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (92.97 W × 5 µs) / 0.15466 J/K = **0.00301°C** = **3.01 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 26,214.4 TMAC/s | 22,282.2 TMAC/s | 239.7 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 119.8 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 59.9 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 30.0 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 15.0 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 400.00 mm² (20.0 mm × 20.0 mm)
* **Wafer Set Consumption:** 5 wafers per run (1 CMOS base + 4 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 28 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 5-wafer stack).

---

### Model 5D: JANUS Datacenter 16-Tile (4-Stratum 3D Datacenter MVP 400.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 16 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 128 × 128 matrix mesh per tile
* **Multiplier Count per Tile:** 128² = 16,384 optical multipliers
* **Total Multipliers on Die:** 16 × 16,384 = **262,144 multipliers**
* **Total Spatial Waveguide Channels:** 262,144 × 256 = **67,108,864 channels** (≈ 67.11 Million)
* **Total Non-Volatile Sb2S3 Switches:** 262,144 × 1,920 = **503,316,480 switches** (≈ 503.32 Million, ≈ 125.83M per stratum)
* **Terminal Ge/Si SAC²M APD Pixels:** 67,108,864 detectors on dedicated 10 µm 2-layer detector block
* **Active Detectors per 10 ps Cycle:** 262,144 active events (131,072 illuminated per 5 ps phase)
* **SiPh Strata Count:** 4 Strata (30 µm each) + Three 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (20.0 mm × 20.0 mm)
* **Die Footprint (A_die):** **400.00 mm²** (20.0 mm × 20.0 mm × 0.58 mm)
* **Switch Footprint per Stratum:** 169.87 mm²
* **Routing Shuffles & Interlayer Vias:** 81.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 75.37 mm²
* **Passive MMI H-Tree & APD Array:** 35.12 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 38.64 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (17 stages of 1:2 MMIs):** L_split,ideal = **51.18 dB**
* **Excess Path Loss (L_excess):** 17 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **14.10 dB**
* **Total Optical Distribution Loss (L_total):** 51.18 dB + 14.10 dB = **65.28 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **46.61 W Optical CW** (+46.69 dBm)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **62.15 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 46.61 W Optical):** 62.15 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 4.10 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 2.62 W
* **Optical Amplification Layer:** 0.00 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 18.52 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **90.39 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 90.39 W / 400.0 mm² = **0.2260 W/mm²** (22.60 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **154.66 mJ/K** (220.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (90.39 W × 5 µs) / 0.15466 J/K = **0.00292°C** = **2.92 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 26,214.4 TMAC/s | 22,282.2 TMAC/s | 246.5 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 123.3 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 61.6 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 30.8 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 1,638.4 TMAC/s | 1,392.6 TMAC/s | 15.41 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 400.00 mm² (20.0 mm × 20.0 mm)
* **Wafer Set Consumption:** 5 wafers per run (1 CMOS base + 4 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 28 Completed Accelerators per Wafer Set** (conserving total active circuit area across the 5-wafer stack).

---

## 7. Generation 6: 5-Stratum 3D Heterogeneous Silicon Photonics & Hyperscale Datacenter (Gen-6)

Generation 6 represents the pinnacle of the JANUS roadmap: the **Datacenter 32-Tile Master Flagship (Model 6A)** deploying over **1.006 Billion PCM switches** on a single 640 mm² die across 5 vertical SiPh strata, and the **Hyperscale Module (Model 6B)** deploying over **2.013 Billion switches** across 64 tiles (1,280 mm²).

### 5-Stratum 11-Layer Monolithic Stack Architecture

```
==================================================================================
  TOP: INTERLEAVED TWO-LAYER Ge/Si SAC²M APD DETECTOR BLOCK (10 µm)
  - 2 Vertically Stacked Ge/Si Sub-Arrays (2 × 5 µm) Handling Alternating Odd/Even Waveguide Channels
  - Dedicated Metal Routing Layers (Halved Pitch, Zero Crosstalk, Direct Contact to HS1)
==================================================================================
  LAYER 10: SiPh STRATUM 5 (30 µm)
  - Dilated Beneš Routing Stages 13-15 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 9.5: INTER-STRATUM SiO2 BUFFER 4 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 9: SiPh STRATUM 4 (30 µm)
  - Dilated Beneš Routing Stages 10-12 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 8.5: INTER-STRATUM SiO2 BUFFER 3 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 8: SiPh STRATUM 3 (30 µm)
  - Dilated Beneš Routing Stages 7-9 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 7.5: INTER-STRATUM SiO2 BUFFER 2 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 7: SiPh STRATUM 2 (30 µm)
  - Dilated Beneš Routing Stages 4-6 (Sb2S3 Switches, 0 W Static Hold)
----------------------------------------------------------------------------------
  LAYER 6.5: INTER-STRATUM SiO2 BUFFER 1 (50 µm)
  - Inter-stratum thermal diffusion time: τ_diff,inter = 2.76 ms (552 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 6: SiPh STRATUM 1 (30 µm)
  - LiTaO3 1x256 Pockels Input Modulators (50 aJ/switch @ 100 GHz)
  - Passive 1064 nm MMI Splitting Tree & Beneš Routing Stages 1-3
----------------------------------------------------------------------------------
  LAYER 2: MONOLITHIC PRIMARY SiO2 THERMAL BUFFER (250 µm)
  - Thermal Diffusivity: α = 9.05 × 10⁻⁷ m²/s | Thermal Diffusion Time: τ_diff = 69.06 ms (13,812 JIR cycles)
----------------------------------------------------------------------------------
  LAYER 1: CMOS BASE LOGIC & CRT RECONSTRUCTION SUBSTRATE (50 µm)
  - StrongARM Regenerative Latches, RNS Encoders & Pipelined CRT Engine
==================================================================================
  TOTAL BARE-DIE ACTIVE 3D STACK HEIGHT: 50 + 250 + 5×30 + 4×50 + 10 = 660 µm (0.66 mm)
==================================================================================
```

---

### Model 6A: JANUS Datacenter 32-Tile (5-Stratum 3D Stack 640.0 mm²)

#### 1. Hardware Architecture & Device Count (From Table XV of main.tex)
* **Residue Tile Count (N_tiles):** 32 independent optical residue tiles
* **Tile Matrix Dimension (N_dim):** 128 × 128 matrix mesh per tile
* **Multiplier Count per Tile:** 128² = 16,384 optical multipliers
* **Total Multipliers on Die:** 32 × 16,384 = **524,288 multipliers**
* **Waveguide Alphabet per Multiplier:** 256 waveguides (One-Hot 8-bit residue representation)
* **Total Spatial Waveguide Channels:** 524,288 × 256 = **134,217,728 channels** (≈ 134.22 Million)
* **Beneš Routing Stages (S):** 2·log₂(256) - 1 = **15 stages**
* **Switches per Multiplier Fabric:** (256/2) × 15 = 128 × 15 = **1,920 switches**
* **Total Non-Volatile Sb2S3 Switches:** 524,288 × 1,920 = **1,006,632,960 switches** (**1.0066 Billion switches**, ≈ 201.33M per stratum)
* **Terminal Ge/Si SAC²M APD Pixels:** 134,217,728 detectors on dedicated 10 µm 2-layer detector block (≈ 134.22 Million)
* **Active Detectors per 10 ps Cycle:** 524,288 active events (262,144 illuminated per 5 ps phase)
* **SiPh Strata Count:** 5 Strata (30 µm each) + Four 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (25.30 mm × 25.30 mm)
* **Die Footprint (A_die):** **640.00 mm²** (25.30 mm × 25.30 mm × 0.66 mm)
* **Switch Footprint per Stratum:** 271.80 mm²
* **Routing Shuffles & Interlayer Vias:** 140.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 120.60 mm²
* **Passive MMI H-Tree & APD Array:** 56.20 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 51.40 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (18 stages of 1:2 MMIs for 262,144 branches):** L_split,ideal = 10·log₁₀(2¹⁸) = **54.19 dB**
* **Excess Path Loss (L_excess):** 18 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **14.40 dB**
* **Total Optical Distribution Loss (L_total):** 54.19 dB + 14.40 dB = **68.59 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **100.00 W Optical CW** (+50.00 dBm, from Table XV of main.tex)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **133.33 Watts**

#### 4. Full-System Electrical Power Breakdown (From Table XV of main.tex)
* **1064 nm Master Laser (75% WPE, 100 W Optical):** 133.33 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 8.19 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 5.24 W
* **Optical Amplification Layer:** 0.00 W
* **PCM Routing Switches (Static Hold):** 0.00 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 37.03 W
* **JIR Scheduler & Control Logic:** 3.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **186.79 Watts** (Operating band: 186.8–200.0 W)

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 186.79 W / 640.0 mm² = **0.2919 W/mm²** (29.19 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **247.46 mJ/K** (352.0 mg mass)
* **Main Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (186.79 W × 5 µs) / 0.24746 J/K = **0.00377°C** = **3.77 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 52,428.8 TMAC/s | 44,564.5 TMAC/s | 238.6 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 26,214.4 TMAC/s | 22,282.2 TMAC/s | 119.3 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 59.6 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 29.8 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 3,276.8 TMAC/s | 2,785.3 TMAC/s | 14.91 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Die Footprint per Stacked Unit:** 640.00 mm² (25.30 mm × 25.30 mm)
* **Wafer Set Consumption:** 6 wafers per run (1 CMOS base + 5 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 14 Completed Hyperscale Accelerators per Wafer Set** (conserving total active circuit area across the 6-wafer stack).

---

### Model 6B: JANUS Datacenter 64-Tile Hyperscale Module (1,280.0 mm²)

#### 1. Hardware Architecture & Device Count
* **Residue Tile Count (N_tiles):** 64 independent optical residue tiles (Dual-Reticle Stitched)
* **Tile Matrix Dimension (N_dim):** 128 × 128 matrix mesh per tile
* **Multiplier Count per Tile:** 128² = 16,384 optical multipliers
* **Total Multipliers on Die:** 64 × 16,384 = **1,048,576 multipliers** (**1.048 Million multipliers**)
* **Total Spatial Waveguide Channels:** 1,048,576 × 256 = **268,435,456 channels** (≈ 268.44 Million)
* **Total Non-Volatile Sb2S3 Switches:** 1,048,576 × 1,920 = **2,013,265,920 switches** (**2.013 Billion switches**, ≈ 402.65M per stratum)
* **Terminal Ge/Si SAC²M APD Pixels:** 268,435,456 detectors on dedicated 10 µm 2-layer detector block (≈ 268.44 Million)
* **Active Detectors per 10 ps Cycle:** 1,048,576 active events (524,288 illuminated per 5 ps phase)
* **SiPh Strata Count:** 5 Strata (30 µm each) + Four 50 µm Inter-Stratum Buffers + 10 µm APD Block

#### 2. Physical Layout & Area Budget (35.78 mm × 35.78 mm)
* **Module Footprint (A_die):** **1,280.00 mm²** (35.78 mm × 35.78 mm × 0.66 mm)
* **Switch Footprint per Stratum:** 543.60 mm²
* **Routing Shuffles & Interlayer Vias:** 280.00 mm²
* **Active LiTaO₃ Input Routers (Stratum 1):** 241.20 mm²
* **Passive MMI H-Tree & APD Array:** 112.40 mm²
* **Perimeter Cu Shunt, Guard Rings & Dicing:** 102.80 mm²

#### 3. Optical Link Budget & Laser Requirement (1064 nm)
* **Passive Split Tree (19 stages of 1:2 MMIs for 524,288 branches):** L_split,ideal = 10·log₁₀(2¹⁹) = **57.20 dB**
* **Excess Path Loss (L_excess):** 19 × 0.30 dB (MMIs) + 7.50 dB (Beneš) + 1.50 dB (Interlayer/Prop) = **14.70 dB**
* **Total Optical Distribution Loss (L_total):** 57.20 dB + 14.70 dB = **71.90 dB**
* **Delivered Receiver Power / Sensitivity:** P_det = **-18.59 dBm** | P_sens = **-23.20 dBm** (Margin = **+4.61 dB**)
* **Master Laser Optical Power (P_laser,opt):** **214.08 W Optical CW** (+53.31 dBm, or dual 107 W Yb-fiber sources)
* **Laser Wall-Plug Electrical Power (>75% WPE):** **285.44 Watts**

#### 4. Full-System Electrical Power Breakdown
* **1064 nm Master Laser (75% WPE, 214.08 W Optical):** 285.44 W
* **LiTaO₃ Pockels Input Routers (100 GHz):** 16.38 W
* **Ge/Si SAC²M APD + StrongARM Readout:** 10.48 W
* **CMOS Encoders, CRT Adder Trees & Adders:** 74.06 W
* **JIR Scheduler & Control Logic:** 6.00 W
* **TOTAL SYSTEM ELECTRICAL POWER:** **392.36 Watts**

#### 5. Thermal Dissipation & Buffer Physics
* **Surface Heat Flux Density (q″):** 392.36 W / 1,280.0 mm² = **0.3065 W/mm²** (30.65 W/cm²)
* **Main SiO₂ Buffer Heat Capacity (C_SiO₂):** **494.91 mJ/K** (704.0 mg mass)
* **Thermal Diffusion Time Constant (τ_diff):** **69.06 ms** = **13,812 JIR cycles**
* **Per-Cycle Temperature Rise (ΔT_cycle):** (392.36 W × 5 µs) / 0.49491 J/K = **0.00396°C** = **3.96 mK**

#### 6. Multi-Precision Performance Matrix (100 GHz)

| Precision Target | RNS Tiles (k) | Peak Throughput | Sustained (η=0.85) | Energy Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **INT4 Direct** | 1 tile | 104,857.6 TMAC/s | 89,129.0 TMAC/s | 227.2 TMAC/s/W |
| **INT8 Exact** | 2 tiles | 52,428.8 TMAC/s | 44,564.5 TMAC/s | 113.6 TMAC/s/W |
| **INT16 Exact** | 4 tiles | 26,214.4 TMAC/s | 22,282.2 TMAC/s | 56.8 TMAC/s/W |
| **INT32 Exact** | 8 tiles | 13,107.2 TMAC/s | 11,141.1 TMAC/s | 28.4 TMAC/s/W |
| **INT64 Exact** | 16 tiles | 6,553.6 TMAC/s | 5,570.6 TMAC/s | 14.20 TMAC/s/W |

#### 7. Foundry Wafer Set Economics (300 mm Silicon Line)
* **Module Footprint per Stacked Unit:** 1,280.00 mm² (35.78 mm × 35.78 mm)
* **Wafer Set Consumption:** 6 wafers per run (1 CMOS base + 5 SiPh strata)
* **Effective Finished Chip Yield:** **≈ 7 Completed Hyperscale Modules per Wafer Set** (conserving total active circuit area across the 6-wafer stack).

---
*Roadmap finalized and approved for engineering architecture, hardware realization, and patent portfolio alignment.*
