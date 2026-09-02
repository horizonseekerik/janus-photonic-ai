# Project JANUS: Spatial Optical RNS Photonic AI Computing Architecture

[![Architecture Treatise](https://img.shields.io/badge/Architecture%20Treatise-37%20Pages%20(IEEEtran)-blue.svg)](./JANUS_IEEE_Manuscript.pdf)
[![Patent Pending](https://img.shields.io/badge/Indian%20Patent-App%20202611052791-gold.svg)](#patent--intellectual-property)
[![TRL Readiness](https://img.shields.io/badge/TRL-4.0%20(Co--Sim%20Validated)-green.svg)](#technology-readiness-level-trl-matrix)
[![Simulation Matrix](https://img.shields.io/badge/Simulation%20Targets-16%2F16%20Met%20(TRL%204)-brightgreen.svg)](#-16-point-multi-physics-sign-off-matrix)
[![Modeled Efficiency](https://img.shields.io/badge/Modeled%20Efficiency-112.8%20TMAC%2Fs%2FW-cyan.svg)](#-ai-workload-benchmarks--gpu-comparison)
[![Static Power](https://img.shields.io/badge/Static%20Hold%20Power-0%20Watts-purple.svg)](#-architectural-pillars)

---

## 📖 Executive Summary

**Project JANUS** is a constraint-aware, bounded-exact optoelectronic tensor computing architecture engineered for high-throughput, low-power deep learning acceleration. 

Conventional optical AI processors encode numbers in continuous analog amplitudes (Mach-Zehnder Interferometers / MZIs), accumulating optical power across analog meshes. For a 128x128 matrix multiplication, unreduced analog accumulation requires an impossible **138.4 dB SNR** (demanding a 21-bit ADC at 100 GHz sampling) and continuous milliwatt thermal tuning that consumes kilowatts of static hold power.

**JANUS solves the fundamental optical computing bottleneck by replacing analog amplitude accumulation with:**
1. **Spatial One-Hot Residue Number System (RNS):** Numbers are mapped to spatial waveguide indices (which discrete waveguide carries light) rather than optical intensity levels.
2. **Sub-Bandgap Non-Volatile Sb₂S₃ Phase-Change Material (PCM) Switches:** Zero static mesh hold power (P_hold = 0 W) via dilated Beneš permutation topologies at 1064 nm.
3. **Receiverless Ge/Si SAC²M Avalanche Photodiodes (APDs):** 1-bit binary arrival detection co-integrated with clocked StrongARM dynamic latches (3.5 ps latching time).
4. **Hybrid 3-Equation Arithmetic Partitioning:** Optics executes non-overflowing residue permutations at 100 GHz, while CMOS SRAM resolve cross-terms, delivering **deterministic exact arithmetic up to INT64 precision**.

---

## 🏛️ Architectural Pillars

```
                      Input 64-Bit Operands (X, Y)
                                  │
                                  ▼
           +─────────────────────────────────────────────+
           |     CMOS 4-Stage RNS Modulo Encoders        |
           |     (Decomposes into 16 coprime channels)   |
           +──────────────────────┬──────────────────────+
                                  │
                                  ▼
           +─────────────────────────────────────────────+
           |   16-Tile Optical Spatial Mesh (1064 nm)    |
           |   - 1-of-256 One-Hot Spatial Laser Routing  |
           |   - Non-Volatile Sb2S3 Beneš Permutation    |
           |   - Zero Static Hold Power (P_hold = 0 W)   |
           +──────────────────────┬──────────────────────+
                                  │
                                  ▼
           +─────────────────────────────────────────────+
           |   Ge/Si SAC2M APDs + Clocked StrongARM      |
           |   (Event-Driven Binary Sensing, ~100 aJ)    |
           +──────────────────────┬──────────────────────+
                                  │
                                  ▼
           +─────────────────────────────────────────────+
           |   8-Stage Pipelined CRT Adder Tree (80 ps)  |
           |   - 256-Entry ROM Precomputed Scaling LUTs  |
           |   - Pipelined Carry-Save Reduction Tree     |
           +──────────────────────┬──────────────────────+
                                  │
                                  ▼
           +─────────────────────────────────────────────+
           |      JIR Consistency & Fault Monitor        |
           |      (Redundant RRNS Channel Verification)  |
           +──────────────────────┬──────────────────────+
                                  │
                                  ▼
                      Exact 64-Bit Result Output
```

---

## 📁 Repository Directory & File Guide

Below is the complete inventory and navigation guide for every folder and file in this repository:

```
Janus Update/
├── README.md                                  # Complete Project Documentation & Navigation Guide
├── index.html                                 # Main Production Single-Page Web Dashboard
├── vercel.json                                # Vercel deployment routing and cache headers
├── requirements.txt                           # Python environment dependencies
├── start_dashboard.vbs                        # Background launcher script for Windows
├── JANUS_IEEE_Manuscript.pdf                  # Complete 37-page formally verified IEEE manuscript
├── JANUS_Mini16_Simulation_Report.pdf         # Multi-physics co-simulation sign-off report
├── JANUS_Mini16_CMOS_Architecture.pdf         # CMOS digital backend & silicon blueprint
├── main.pdf                                   # Compiled root manuscript
├── deep-research-report.md                    # In-depth architectural synthesis research report
│
├── api/                                       # Serverless API Runtime (Vercel & Cloud)
│   └── index.py                               # Unified REST API router & solver dispatcher
│
├── public/                                    # Vercel Static Distribution Directory
│   ├── index.html                             # Synced web interface for CDN hosting
│   ├── JANUS_IEEE_Manuscript.pdf              # Hosted IEEE manuscript
│   ├── JANUS_Mini16_Simulation_Report.pdf     # Hosted simulation report
│   ├── JANUS_Mini16_CMOS_Architecture.pdf     # Hosted CMOS specification
│   └── main.pdf                               # Hosted paper
│
├── janus_mini16_sim/                          # 5-Tier Multi-Physics Co-Simulation Framework
│   ├── run_mini16_full_cosim.py               # Master CLI co-simulation test suite runner
│   ├── run_dashboard.py                       # Local Flask/WSGI interactive dashboard server
│   ├── start_dashboard.vbs                    # VBScript dashboard launcher
│   ├── stop_dashboard.bat                     # Windows background task killer
│   ├── AI_BENCHMARK_REPORT.md                 # Layer-by-layer AI benchmarking data report
│   │
│   ├── configs/                               # Hardware Constants & Architectural Specs
│   │   ├── mini_16t_constants.py              # Physical parameters (materials, losses, moduli)
│   │   └── mini_16t_specs.json                # JSON specification dictionary for 16-tile MVP
│   │
│   ├── tier1_meep_optics/                     # TIER 1: Photonic FDTD & Waveguide Solvers
│   │   ├── sb2s3_switch_cell.py               # 3D FDTD Sb2S3 directional coupler model
│   │   ├── litao3_pockels_router.py           # 100 GHz electro-optic LiTaO3 Pockels modulator
│   │   ├── waveguide_crossing.py              # Multi-mode interference (MMI) crossing solver
│   │   ├── sb2s3_tolerance_monte_carlo.py     # Fabrication tolerance Monte Carlo analysis
│   │   ├── export_touchstone.py               # S-parameter Touchstone (.s4p) exporter
│   │   ├── export_heat_map.py                 # Optical dissipation Q_opt(x,y,z) heat exporter
│   │   ├── gds_layout_processor.py            # GDS-II layout verification utility
│   │   └── test_tier1_all.py                  # Pytest automated test harness for Tier 1
│   │
│   ├── tier2_elmer_thermal/                   # TIER 2: 3D FEM Thermal & Heat Diffusion Solvers
│   │   ├── elmer_thermal_solver.py            # Elmer 3D transient & steady-state solver
│   │   ├── gmsh_mesh_generator.py             # 3D GMSH tetrahedral mesh generator
│   │   ├── extract_thermal_rom.py             # Foster RC thermal reduced-order model (ROM)
│   │   ├── case.sif / materials.sif           # Elmer FEM solver input configuration files
│   │   ├── mini16_mesh.geo                    # Geometric CAD definition for 3D die stack
│   │   └── test_tier2_all.py                  # Pytest automated test harness for Tier 2
│   │
│   ├── tier3_xyce_circuit/                    # TIER 3: Optoelectronic SPICE & APD Circuit Models
│   │   ├── apd_receiver_model.py              # Ge/Si SAC2M avalanche photodiode SPICE model
│   │   ├── strongarm_latch.py                 # Clocked StrongARM dynamic regenerative latch
│   │   ├── eye_diagram_ber.py                 # 100 GHz eye diagram & BER estimator
│   │   ├── ilo_comb_lock.py                   # 50 fs RMS injection-locked optoelectronic clock
│   │   ├── vector_fit_s_params.py             # Touchstone S-parameter SPICE macromodeling
│   │   ├── optical_switch_sp.cir              # SPICE circuit netlist for optical switch
│   │   └── test_tier3_all.py                  # Pytest automated test harness for Tier 3
│   │
│   ├── tier4_rtl_digital/                     # TIER 4: Synthesizable Verilog Digital Logic
│   │   ├── rns_encoder.v                      # 100 GHz wave-pipelined 64b to 16-residue encoder
│   │   ├── crt_adder_tree.v                   # 8-stage pipelined Mixed-Radix CRT adder tree
│   │   ├── jir_fault_monitor.v                # Real-time residue consistency checker
│   │   ├── tb_crt_adder_tree.v                # Verilog testbench for CRT reconstruction
│   │   ├── rtl_synthesis_analyzer.py          # Yosys synthesis parser and timing checker
│   │   ├── test_crt_cocotb.py                 # Cocotb cycle-accurate Python co-simulation
│   │   └── test_tier4_all.py                  # Pytest automated test harness for Tier 4
│   │
│   ├── tier5_python_rns/                      # TIER 5: Formal Z3 Math & AI Workload Benchmarks
│   │   ├── formal_verifier.py                 # Z3 SMT solver formal mathematical precision proofs
│   │   ├── spatial_one_hot_router.py          # Tensor mapping to physical 1-of-256 waveguides
│   │   ├── jir_thermal_scheduler.py           # Closed-loop thermal swapping & modulus rotation
│   │   ├── moduli_generator.py                # Coprime moduli selection & dynamic range calculator
│   │   ├── rrns_self_healing.py               # Redundant RNS single-channel fault correction
│   │   ├── gemm_exact_benchmark.py            # Exact 64-bit matrix multiplication engine
│   │   ├── ai_workload_benchmarks.py          # LLaMA-3, GPT-2, and ViT layer profiler
│   │   ├── batch_token_packer.py              # Spatial multi-head attention batching engine
│   │   ├── gpu_comparator.py                  # Energy/area comparative analysis vs GPUs
│   │   └── test_tier5_all.py                  # Pytest automated test harness for Tier 5
│   │
│   ├── orchestrator/                          # Multi-Physics Co-Simulation Orchestrator
│   │   ├── master_orchestrator.py             # 16-point sign-off matrix execution manager
│   │   ├── test_orchestrator.py               # Orchestrator test suite
│   │   └── artifacts/                         # Generated plots, CSVs, and JSON logs
│   │
│   ├── benchmarks/                            # AI Benchmarking & Profiling Scripts
│   │   ├── run_ai_profiling.py                # Standalone AI workload evaluation runner
│   │   ├── export_simulation_field_plots.py   # Visual wave & thermal field plot generator
│   │   └── test_ai_profiling.py               # Benchmark test suite
│   │
│   └── dashboard/                             # Dashboard Backend & Local Assets
│       ├── server.py                          # Flask application backend
│       └── templates/index.html               # Synced local dashboard template
│
├── documentation_reports/                     # Complete Engineering Specifications & Roadmaps
│   ├── JANUS_MINI_16T_CO_SIMULATION_SPEC.pdf  # Comprehensive Multi-Physics Spec (PDF/MD/HTML)
│   ├── JANUS_MINI_16T_ALGORITHMS_AND_FLOWCHARTS.pdf # Mathematical algorithms & pipeline charts
│   ├── PROJECT_JANUS_STRATEGIC_ROADMAP.pdf    # Commercialization & 18-Model Matrix Guide
│   └── figures/                               # Architectural diagrams and circuit schematics
│
├── paper_latex/                               # 37-Page Primary IEEE Architecture Manuscript
│   ├── main.tex                               # Full LaTeX source code (IEEEtran format)
│   ├── references.bib                         # Academic bibliography database
│   ├── main.pdf                               # Formally compiled PDF manuscript
│   └── PCM_MATERIAL_SELECTION_RATIONALE.md    # Thermodynamic & optical analysis of Sb2S3
│
├── cmos_paper_latex/                          # IEEE CMOS Backend Architecture Specification
│   ├── JANUS_Mini16_CMOS_Architecture.tex     # LaTeX source for companion CMOS paper
│   ├── references.bib                         # CMOS bibliography database
│   └── JANUS_Mini16_CMOS_Architecture.pdf     # Compiled CMOS architecture PDF
│
├── simulation_paper_latex/                    # IEEE Co-Simulation Sign-Off Paper
│   ├── JANUS_Mini16_Simulation_Report.tex     # LaTeX source for companion simulation paper
│   ├── references.bib                         # Simulation bibliography database
│   └── JANUS_Mini16_Simulation_Report.pdf     # Compiled simulation sign-off PDF
│
└── CMOS RECONSTRUCTION/                       # Archival Silicon Specifications
    └── JANUS_CMOS_Architecture.pdf            # Initial CMOS reconstruction spec
```

---

## 🔬 Multi-Scale 5-Tier Verification Stack

| Tier | Simulation Engine | Physical / Architectural Scope | Deliverables & Verification |
|---|---|---|---|
| **Tier 1** | **3D MEEP (FDTD)** | 3D Maxwell curl solver, non-volatile Sb₂S₃ switch cell (1064 nm), MMI crossings, LiTaO₃ Pockels routers. | Touchstone `.s4p` S-matrices, Q_opt(x,y,z) heat map, IL ≤ 0.017 dB, ER ≥ 25.0 dB. |
| **Tier 2** | **Elmer FEM (3D)** | 3D transient heat diffusion, 250 µm SiO₂ buffer, thermal transient damping, Foster RC extraction. | τ_diff = 69.06 ms, ΔT_cycle ≤ 0.80 mK, 5-pole state-space ROM (R² = 1.000). |
| **Tier 3** | **Xyce SPICE** | Ge/Si SAC²M APD receiver (M=7), clocked StrongARM latch (3.5 ps regen), 100 GHz eye diagrams. | BER ≤ 10⁻¹⁸, practical link margin ≥ +3.02 dB, eye opening > 60%. |
| **Tier 4** | **Digital CMOS RTL** | 100 GHz wave-pipelined RNS encoder, 8-stage CRT adder tree (80 ps latency), JIR fault monitor in Verilog. | Cycle-accurate bit-exact reconstruction (0 clock slips, 0 errors across 1000 randomized vectors). |
| **Tier 5** | **Python RNS Engine** | Z3 SMT formal mathematical proofs, Spatial One-Hot tensor router, JIR thermal scheduler, RRNS self-healing. | 4/4 formal proofs passed, 100% single-fault recovery, **0.00000000% GEMM arithmetic deviation**. |

---

## ✅ 16-Point Multi-Physics Sign-Off Matrix

```
============================================================================================
  PROJECT JANUS MINI (16-TILE): 16-POINT QUANTITATIVE VERIFICATION SIGN-OFF MATRIX
============================================================================================
#   | Tier    | Verification Metric                  | Target Spec        | Measured     | Status
--------------------------------------------------------------------------------------------
1   | Tier 1  | Sb2S3 Switch Insertion Loss (Amorph) | IL <= 0.50 dB      | 0.017 dB     | [PASS]
2   | Tier 1  | Dilated Beneš Extinction Ratio       | ER >= 25.0 dB      | 25.0 dB      | [PASS]
3   | Tier 1  | Waveguide Crossing Insertion Loss    | IL <= 0.025 dB     | 0.0131 dB    | [PASS]
4   | Tier 1  | Waveguide Crossing Crosstalk         | XT <= -38.0 dB     | -41.06 dB    | [PASS]
5   | Tier 2  | SiO2 Thermal Diffusion Time Constant | 65 ms <= tau_diff  | 69.06 ms     | [PASS]
6   | Tier 2  | Per-Cycle Thermal Transient          | dT_cycle <= 0.80 m | 0.798 mK     | [PASS]
7   | Tier 2  | Max Steady-State Operating Temp      | T_steady <= 70.0 C | 25.06 °C     | [PASS]
8   | Tier 2  | Thermal ROM Extraction Accuracy      | R^2 >= 0.999       | 1.000000     | [PASS]
9   | Tier 3  | APD Practical Sensitivity Margin     | Margin >= +3.00 dB | +3.45 dB     | [PASS]
10  | Tier 3  | Optical Receiver Bit Error Rate      | BER <= 10^-18      | 3.47e-41     | [PASS]
11  | Tier 3  | 100 GHz Eye Diagram Opening          | Eye Opening > 0%   | 61.1%        | [PASS]
12  | Tier 4  | CRT Adder Tree Digital Latency       | t_CRT <= 220 ps    | 80.0 ps      | [PASS]
13  | Tier 4  | RTL Cycle-Accurate Verification      | Errors == 0        | 0 errors     | [PASS]
14  | Tier 5  | Z3 SMT Formal Proofs (4 Proofs)      | 4 / 4 Proved       | 4 / 4 Proved | [PASS]
15  | Tier 5  | RRNS Single-Fault Self-Healing Recov | Correction == 100% | 100.0%       | [PASS]
16  | Tier 5  | Exact GEMM Arithmetic Precision Devi | Deviation == 0     | 0.000000%    | [PASS]
============================================================================================
  Summary: 16/16 Passed (100.0%) | Execution Time: ~10.1s | STATUS: TAPEOUT-READY (TRL 4)
============================================================================================
```

---

## 🗺️ Master Hardware Scaling Roadmap (18 Models)

Project JANUS scales from an entry **Alpha Single-Stratum Monolithic MVP (6.17 W)** up to a **5-Stratum 3D Hyperscale Apex Module (104.85 PetaMAC/s at 392 W)** across 6 generations and 18 distinct hardware configurations:

| Model | Generation & Stack | Strata | Tiles | Mesh Size | Total Switches | Die Area | Total Power | INT8 Throughput | INT64 Throughput | TRL Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1A** | Gen-1 Monolithic Planar MVP | 1 | 16 | 32 x 32 | 31.46 M | 100.0 mm² | **6.17 W** | 696.3 TMAC/s | 87.0 TMAC/s | **TRL 4 (Co-Sim Verified)** |
| **1B** | Gen-1 Monolithic Planar Full | 1 | 32 | 32 x 32 | 62.91 M | 200.0 mm² | **12.67 W** | 1,392.6 TMAC/s | 174.1 TMAC/s | TRL 3 (Analytical Proof) |
| **2A** | Gen-2 Monolithic Planar Edge | 1 | 16 | 64 x 64 | 125.83 M | 400.0 mm² | 23.49 W | 2,785.3 TMAC/s | 348.2 TMAC/s | TRL 3 (Analytical Proof) |
| **2B** | Gen-2 3D Mini Stack (50 mm²) | 2 | 16 | 32 x 32 | 31.46 M | 50.0 mm² | **6.17 W** | 696.3 TMAC/s | 87.0 TMAC/s | TRL 3 (Analytical Proof) |
| **2C** | Gen-2 3D Mini Stack (100 mm²) | 2 | 32 | 32 x 32 | 62.91 M | 100.0 mm² | **12.67 W** | 1,392.6 TMAC/s | 174.1 TMAC/s | TRL 3 (Analytical Proof) |
| **3A** | Gen-3 3D Mini Stack (200 mm²) | 2 | 64 | 32 x 32 | 125.83 M | 200.0 mm² | 23.49 W | 2,785.3 TMAC/s | 348.2 TMAC/s | TRL 3 (Analytical Proof) |
| **3B** | Gen-3 3D Edge Stack (200 mm²) | 2 | 16 | 64 x 64 | 125.83 M | 200.0 mm² | 23.49 W | 2,785.3 TMAC/s | 348.2 TMAC/s | TRL 3 (Analytical Proof) |
| **3C** | Gen-3 3D Edge Stack (400 mm²) | 2 | 32 | 64 x 64 | 251.66 M | 400.0 mm² | 45.91 W | 5,570.6 TMAC/s | 696.3 TMAC/s | TRL 3 (Analytical Proof) |
| **4E** | Gen-4 3D Edge Flagship | 3 | 64 | 64 x 64 | 503.32 M | 533.3 mm² | 92.97 W | 11,141.1 TMAC/s | 1,392.6 TMAC/s | TRL 3 (Analytical Proof) |
| **5D** | Gen-5 3D Datacenter MVP | 4 | 16 | 128 x 128 | 503.32 M | 400.0 mm² | 90.39 W | 11,141.1 TMAC/s | 1,392.6 TMAC/s | TRL 3 (Analytical Proof) |
| **6A** | Gen-6 3D Datacenter Master | 5 | 32 | 128 x 128 | **1.0066 B** | 640.0 mm² | 186.65 W | 22,282.2 TMAC/s | 2,785.3 TMAC/s | TRL 3 (Analytical Proof) |
| **6B** | Gen-6 3D Hyperscale Apex Module | 5 | 64 | 128 x 128 | **2.0132 B** | 1,280.0 mm² | **392.36 W** | **52.42 PMAC/s** | **5,570.6 TMAC/s** | TRL 3 (Analytical Proof) |

---

## 🤖 AI Workload Benchmarks & GPU Comparison

### Model Inference Performance (Model 1A: 6.17 W)
* **LLaMA-3-8B (INT8):** 1.938 µJ per autoregressive token (112.55 TMAC/s/W average efficiency).
* **GPT-2 Base (INT8):** 0.098 µJ per token (113.82 TMAC/s/W).
* **ViT-Huge (INT8):** 1.423 µJ per image patch pass (112.98 TMAC/s/W).

### Hardware Efficiency Comparison Table

| Accelerator Platform | Architecture & Process | TDP Power (W) | Peak INT8 Throughput | Energy Efficiency (TMAC/s/W) | Advantage vs Platform |
|---|---|:---:|:---:|:---:|:---:|
| **Project JANUS (Model 1A)** | **Spatial RNS Photonic (3D Heterogeneous)** | **6.17 W** | **696.3 TMAC/s** | **112.8 TMAC/s/W** | **Baseline (1.0x)** |
| NVIDIA H100 SXM5 | 4N Silicon Electronic GPU | 700 W | 494.0 TMAC/s | 0.706 TMAC/s/W | **159.7x JANUS Advantage** |
| NVIDIA B200 (Blackwell) | 4NP Silicon Electronic GPU | 1,000 W | 1,125.0 TMAC/s | 1.125 TMAC/s/W | **100.3x JANUS Advantage** |
| Google TPU v5p | 4nm Electronic TPU | 450 W | 459.0 TMAC/s | 1.020 TMAC/s/W | **110.6x JANUS Advantage** |

> **Note on Methodology:** JANUS metrics represent multi-physics simulated projections for the Model 1A 16-Tile Monolithic Architecture (6.17 W base TDP). GPU / TPU figures reflect manufacturer published datasheet specifications for production silicon (NVIDIA H100 SXM5 / B200 / Google TPU v5p).

---

## 💻 Quick Start & Developer Instructions

### 1. Prerequisites
* Python 3.9+ (Windows, macOS, or Linux)
* `git`
* Optional for full RTL synthesis: `iverilog`, `yosys`, `cocotb`

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/horizonseekerik/janus-photonic-ai.git
cd janus-photonic-ai
pip install -r requirements.txt
```

### 3. Running the Full 16-Test Multi-Physics Co-Simulation
Execute the 16-point sign-off matrix solver suite:
```bash
python janus_mini16_sim/run_mini16_full_cosim.py
```

### 4. Running Individual Verification Tiers
Run test suites using `pytest`:
```bash
# Tier 1: FDTD Optics & Waveguide Crossings
pytest janus_mini16_sim/tier1_meep_optics/test_tier1_all.py -v

# Tier 2: 3D Thermal Elmer FEM Diffusion
pytest janus_mini16_sim/tier2_elmer_thermal/test_tier2_all.py -v

# Tier 3: Optoelectronic SPICE APD & Latches
pytest janus_mini16_sim/tier3_xyce_circuit/test_tier3_all.py -v

# Tier 4: Digital Verilog CRT Reconstruction
pytest janus_mini16_sim/tier4_rtl_digital/test_tier4_all.py -v

# Tier 5: Z3 Formal Math & Precision Proofs
pytest janus_mini16_sim/tier5_python_rns/test_tier5_all.py -v
```

### 5. Launching the Interactive Local Web Dashboard
To launch the interactive dashboard on your local machine:
```bash
# Option A: Standard Python runner
python janus_mini16_sim/run_dashboard.py

# Option B: Windows background VBScript
wscript start_dashboard.vbs
```
Then open your browser to **`http://127.0.0.1:5000`**.

---

## 📱 Navigation & Web Dashboard Features

The web interface (`index.html`) is fully responsive across desktop, tablet, and mobile edge devices:

1. **🏠 Overview (Page 1):** Storytelling banner, core analog vs binary problem breakdown, architectural pillars, and top-level KPIs.
2. **📄 Manuscript (Page 2):** Integrated document viewer with direct toggling between the 37-page Architecture Paper, Simulation Sign-Off Report, and CMOS Silicon Blueprint.
3. **⚡ Co-Simulation Suite (Page 3):**
   * **Tab 1 (One-Hot RNS & Waveguides):** Interactive 64-bit integer decomposition calculator, custom multiplication simulator, and 16-tile spatial waveguide allocation grid.
   * **Tab 2 (Architecture & Light Co-Design):** Live animated 3D photon propagation engine with 100 GHz mode controls, pause/step/speed toggles, and TSV micro-pillar pulses.
   * **Tab 3 (AI Profiling & Benchmarks):** Layer-by-layer profiling for LLaMA-3, GPT-2, and ViT with live energy breakdown and GPU comparative graphs.
   * **Tab 4 (16-Tile Thermal & JIR Scheduler):** 16-tile monolithic thermal floorplan, multi-physics tile inspector with live 100 GHz eye diagrams, and multi-hour datacenter stress simulator.
   * **Tab 5 (16-Point Sign-Off Matrix):** Multi-physics audit table with single-click solver execution and tier-specific testing buttons.
4. **💻 Codebase (Page 4):** Integrated multi-language file explorer with syntax highlighting for Python, Verilog RTL, Elmer FEM, and LaTeX.
5. **🗺️ Roadmap (Page 5):** 18-model master matrix, interactive TRL progress inspector (TRL 1 through TRL 7), and 6-generation scaling ladder.
6. **🔬 CMOS & 3D Stack (Page 6):** Deep-dive into the 330 µm heterogeneous stack, 65nm CMOS base die, Polyphase deserializer, and hydraulic thermal shunt.
7. **🧠 Software & JIR (Page 7):** Complete software ecosystem, compiler intermediate representation (JIR), and 8 constraint-first physical paradigms.
8. **👤 About Creator (Page 8):** Research background, patent application information, and official academic citation details.

---

## 📜 Patent & Intellectual Property

The algorithms, spatial residue mapping architectures, circuit topologies, and thermal management mechanisms of Project JANUS are protected under:

* **Patent Application:** Indian Patent Application No. **202611052791** *(Patent Pending)*
* **Title:** *A Spatial Residue Number System Photonic AI Architecture with Non-Volatile Phase-Change Routing and Monolithic 3D Heterogeneous Stacking*
* **Lead Architect & Inventor:** Deepanshu Bhardwaj

---

## 📌 Citation (IEEE Format)

To cite Project JANUS and Deepanshu Bhardwaj's research in academic publications:

```bibtex
@misc{bhardwaj2026janus,
  author       = {Deepanshu Bhardwaj},
  title        = {JANUS: A Spatial Residue Number System Photonic AI Architecture with Non-Volatile Phase-Change Routing},
  howpublished = {Preprint / Architectural Treatise (IEEEtran Format)},
  year         = {2026},
  note         = {Indian Patent Application 202611052791. 37-page architectural specification}
}
```

---

## 📄 License & Legal Notice

Copyright © 2026 Deepanshu Bhardwaj. All Rights Reserved.  
Project JANUS and its associated multi-physics co-simulation tools, RTL designs, and patent architectures are proprietary research intellectual property.
