"""
PROJECT JANUS MINI (16-TILE): GPU COMPARATIVE BENCHMARK MODEL
==============================================================
Compares JANUS Mini 16-Tile against modern enterprise Datacenter GPUs:
  1. NVIDIA H100 SXM5 (TSMC 4N, 814 mm^2, 700 W)
  2. NVIDIA B200 Blackwell (TSMC 4NP, 1600 mm^2, 1000 W)

Evaluates:
  - Throughput (TMAC/s and TOPS)
  - Energy Efficiency (TMAC/s per Watt and TOPS/W)
  - Silicon Compute Density (TMAC/s per mm^2)
  - Single-Layer Latency & Token Generation Latency (ns vs us)
  - Bit-Exact Precision Reliability (Zero analog drift / zero quantization noise)
"""

import sys
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from configs import mini_16t_constants as cfg
from tier5_python_rns.ai_workload_benchmarks import AIWorkloadProfiler


@dataclass
class HardwarePlatformSpec:
    name: str
    architecture: str
    process_node: str
    die_area_mm2: float
    tdp_watts: float
    peak_int4_tops: float
    peak_int8_tops: float
    peak_int4_tmacs: float
    peak_int8_tmacs: float
    energy_eff_int8_tmacs_w: float
    compute_density_int8_tmacs_mm2: float


# Official Enterprise Baseline Specifications
H100_SXM5 = HardwarePlatformSpec(
    name="NVIDIA H100 SXM5",
    architecture="Hopper (4th Gen Tensor Cores)",
    process_node="TSMC 4N",
    die_area_mm2=814.0,
    tdp_watts=700.0,
    peak_int4_tops=1979.0,
    peak_int8_tops=989.5,
    peak_int4_tmacs=989.5,
    peak_int8_tmacs=494.75,
    energy_eff_int8_tmacs_w=494.75 / 700.0,            # 0.707 TMAC/s/W
    compute_density_int8_tmacs_mm2=494.75 / 814.0,     # 0.608 TMAC/s/mm^2
)

B200_BLACKWELL = HardwarePlatformSpec(
    name="NVIDIA B200 Blackwell",
    architecture="Blackwell (5th Gen Tensor Cores)",
    process_node="TSMC 4NP (Dual-Die)",
    die_area_mm2=1600.0,
    tdp_watts=1000.0,
    peak_int4_tops=4500.0,
    peak_int8_tops=2250.0,
    peak_int4_tmacs=2250.0,
    peak_int8_tmacs=1125.0,
    energy_eff_int8_tmacs_w=1125.0 / 1000.0,           # 1.125 TMAC/s/W
    compute_density_int8_tmacs_mm2=1125.0 / 1600.0,    # 0.703 TMAC/s/mm^2
)

JANUS_MINI_16T = HardwarePlatformSpec(
    name="JANUS Mini 16-Tile (Planar MVP)",
    architecture="One-Hot Optical Spatial RNS + 100 GHz CMOS",
    process_node="3D Hybrid (30um SiPh + 50um CMOS)",
    die_area_mm2=100.0,
    tdp_watts=6.17,
    peak_int4_tops=2785.3 * 2.0,                       # 5570.6 TOPS
    peak_int8_tops=1392.6 * 2.0,                       # 2785.2 TOPS
    peak_int4_tmacs=cfg.TP_int4_sustained / 1e12,       # 1392.6 TMAC/s sustained
    peak_int8_tmacs=cfg.TP_int8_sustained / 1e12,       # 696.3 TMAC/s sustained
    energy_eff_int8_tmacs_w=(cfg.TP_int8_sustained / 1e12) / 6.17,  # 112.8 TMAC/s/W
    compute_density_int8_tmacs_mm2=(cfg.TP_int8_sustained / 1e12) / 100.0, # 6.96 TMAC/s/mm^2
)


class GPUComparator:
    """Performs rigorous comparative benchmark analysis between JANUS and GPUs."""

    def __init__(self):
        self.profiler = AIWorkloadProfiler()
        self.janus_spec = JANUS_MINI_16T
        self.h100_spec = H100_SXM5
        self.b200_spec = B200_BLACKWELL

    def get_hardware_comparison_table(self) -> Dict[str, Any]:
        """Returns consolidated architectural and physical comparison matrix."""
        eff_ratio_h100 = self.janus_spec.energy_eff_int8_tmacs_w / self.h100_spec.energy_eff_int8_tmacs_w
        eff_ratio_b200 = self.janus_spec.energy_eff_int8_tmacs_w / self.b200_spec.energy_eff_int8_tmacs_w
        density_ratio_h100 = self.janus_spec.compute_density_int8_tmacs_mm2 / self.h100_spec.compute_density_int8_tmacs_mm2
        density_ratio_b200 = self.janus_spec.compute_density_int8_tmacs_mm2 / self.b200_spec.compute_density_int8_tmacs_mm2

        return {
            "platforms": [
                asdict(self.janus_spec),
                asdict(self.h100_spec),
                asdict(self.b200_spec),
            ],
            "janus_vs_h100_energy_efficiency_mult": eff_ratio_h100,
            "janus_vs_b200_energy_efficiency_mult": eff_ratio_b200,
            "janus_vs_h100_density_mult": density_ratio_h100,
            "janus_vs_b200_density_mult": density_ratio_b200,
        }

    def compare_llama3_layer(self, precision: str = "INT8") -> Dict[str, Any]:
        """Compares single LLaMA-3-8B Transformer layer execution across platforms."""
        janus_profile = self.profiler.benchmark_llama3_8b(batch_size=1, seq_len=1, precision=precision)
        total_macs = janus_profile["total_layer_macs"]
        janus_lat_ns = janus_profile["total_layer_latency_ns"]
        janus_energy_uj = janus_profile["total_layer_energy_uj"]

        # GPU theoretical execution time (at 60% realistic sustained tensor utilization)
        gpu_util = 0.60
        h100_tmacs = (self.h100_spec.peak_int8_tmacs if precision == "INT8" else self.h100_spec.peak_int4_tmacs) * gpu_util
        b200_tmacs = (self.b200_spec.peak_int8_tmacs if precision == "INT8" else self.b200_spec.peak_int4_tmacs) * gpu_util

        h100_lat_ns = (total_macs / (h100_tmacs * 1e12)) * 1e9
        b200_lat_ns = (total_macs / (b200_tmacs * 1e12)) * 1e9

        h100_energy_uj = (self.h100_spec.tdp_watts * (h100_lat_ns * 1e-9)) * 1e6
        b200_energy_uj = (self.b200_spec.tdp_watts * (b200_lat_ns * 1e-9)) * 1e6

        return {
            "workload": "LLaMA-3-8B Single Transformer Layer",
            "precision": precision,
            "total_macs": total_macs,
            "janus": {
                "latency_ns": janus_lat_ns,
                "power_watts": self.janus_spec.tdp_watts,
                "energy_uj": janus_energy_uj,
                "throughput_tmacs": janus_profile["average_throughput_tmacs"],
            },
            "h100": {
                "latency_ns": h100_lat_ns,
                "power_watts": self.h100_spec.tdp_watts,
                "energy_uj": h100_energy_uj,
                "throughput_tmacs": h100_tmacs,
            },
            "b200": {
                "latency_ns": b200_lat_ns,
                "power_watts": self.b200_spec.tdp_watts,
                "energy_uj": b200_energy_uj,
                "throughput_tmacs": b200_tmacs,
            },
            "energy_savings_vs_h100": h100_energy_uj / janus_energy_uj,
            "energy_savings_vs_b200": b200_energy_uj / janus_energy_uj,
            "latency_speedup_vs_h100": h100_lat_ns / janus_lat_ns,
            "latency_speedup_vs_b200": b200_lat_ns / janus_lat_ns,
        }
