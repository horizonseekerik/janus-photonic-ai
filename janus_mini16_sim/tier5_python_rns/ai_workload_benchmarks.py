"""
PROJECT JANUS MINI (16-TILE): AI WORKLOAD BENCHMARKING ENGINE
==============================================================
Profiles real-world Deep Learning and Generative AI model layers (LLaMA-3-8B, GPT-4, ViT)
across the 16-tile spatial One-Hot RNS accelerator.

Calculates:
  - Tiling decomposition across 16 (32x32) optical residue tiles
  - Wave-pipelined execution cycles and physical latency (100 GHz, 10 ps cycle)
  - JIR thermal rotation duty-cycle latency (eta = 0.85)
  - Energy per layer and energy per token
  - Bit-exact numerical verification of partitioned GEMM blocks
"""

import sys
import os
import math
from dataclasses import dataclass, asdict
from typing import Dict, Any
import numpy as np

# Add parent directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from configs import mini_16t_constants as cfg
from tier5_python_rns.spatial_one_hot_router import SpatialOneHotAccelerator
from tier5_python_rns.moduli_generator import generate_moduli_set


@dataclass
class LayerBenchmarkResult:
    model_name: str
    layer_name: str
    precision: str
    M: int
    K: int
    N: int
    total_macs: int
    num_tile_blocks: int
    tiles_per_op: int
    num_parallel_engines: int
    execution_cycles: int
    raw_latency_ns: float
    sustained_latency_ns: float
    throughput_tmacs: float
    energy_uj: float
    energy_efficiency_tmacs_w: float
    bit_exact_verified: bool


class AIWorkloadProfiler:
    """Profiles real AI model layers on the JANUS Mini 16-Tile hardware architecture."""

    def __init__(self):
        self.N_tiles = cfg.N_tiles  # 16 tiles
        self.N_dim = cfg.N_dim      # 32x32 mesh per tile
        self.f_clk = cfg.f_clk      # 100 GHz
        self.T_cycle = cfg.T_cycle  # 10.0 ps
        self.eta = cfg.eta_sustained # 0.85 (JIR thermal rotation duty cycle)
        self.P_total = cfg.P_total_system # 6.17 W

        self.mod_info = generate_moduli_set()
        self.accelerator = SpatialOneHotAccelerator()

    def get_tiles_needed(self, precision: str) -> int:
        """Returns physical residue tiles needed per multiplication according to word width."""
        p_map = {
            "INT4": 1,
            "INT8": 2,
            "INT16": 4,
            "INT32": 8,
            "INT64": 16,
        }
        return p_map.get(precision.upper(), 2)

    def profile_layer(
        self,
        model_name: str,
        layer_name: str,
        M: int,
        K: int,
        N: int,
        precision: str = "INT8",
        verify_sample: bool = True,
    ) -> LayerBenchmarkResult:
        """
        Profiles a single GEMM layer of dimension (M x K) @ (K x N).
        """
        total_macs = M * K * N
        k_tiles = self.get_tiles_needed(precision)
        n_engines = self.N_tiles // k_tiles

        # Number of 32x32 tile operations
        blocks_M = math.ceil(M / self.N_dim)
        blocks_K = math.ceil(K / self.N_dim)
        blocks_N = math.ceil(N / self.N_dim)
        total_tile_blocks = blocks_M * blocks_K * blocks_N

        # Pipeline cycles: wave-pipelined queue + pipeline fill/drain depth (12 cycles)
        execution_cycles = math.ceil(total_tile_blocks / n_engines) + 12
        raw_latency_s = execution_cycles * self.T_cycle
        sustained_latency_s = raw_latency_s / self.eta

        raw_latency_ns = raw_latency_s * 1e9
        sustained_latency_ns = sustained_latency_s * 1e9

        # Throughput & Energy
        throughput_tmacs = (total_macs / sustained_latency_s) / 1e12
        energy_j = self.P_total * sustained_latency_s
        energy_uj = energy_j * 1e6
        efficiency_tmacs_w = throughput_tmacs / self.P_total

        # Verify bit-exact correctness on sample block if requested
        bit_exact = True
        if verify_sample:
            A_sample = np.random.randint(0, 50, size=(self.N_dim, self.N_dim))
            B_sample = np.random.randint(0, 50, size=(self.N_dim, self.N_dim))
            C_opt = self.accelerator.matmul(A_sample, B_sample)
            C_ref = np.matmul(A_sample.astype(object), B_sample.astype(object))
            diff = int(np.sum(np.abs(C_opt - C_ref)))
            bit_exact = (diff == 0)

        return LayerBenchmarkResult(
            model_name=model_name,
            layer_name=layer_name,
            precision=precision.upper(),
            M=M,
            K=K,
            N=N,
            total_macs=total_macs,
            num_tile_blocks=total_tile_blocks,
            tiles_per_op=k_tiles,
            num_parallel_engines=n_engines,
            execution_cycles=execution_cycles,
            raw_latency_ns=raw_latency_ns,
            sustained_latency_ns=sustained_latency_ns,
            throughput_tmacs=throughput_tmacs,
            energy_uj=energy_uj,
            energy_efficiency_tmacs_w=efficiency_tmacs_w,
            bit_exact_verified=bit_exact,
        )

    def benchmark_llama3_8b(self, batch_size: int = 1, seq_len: int = 1, precision: str = "INT8") -> Dict[str, Any]:
        """
        Profiles a full LLaMA-3-8B Transformer Layer (32 heads, hidden_dim=4096, intermediate_dim=14336).
        """
        hidden_dim = 4096
        intermediate_dim = 14336
        M = batch_size * seq_len

        layers = [
            ("Q_Projection", M, hidden_dim, hidden_dim),
            ("K_Projection", M, hidden_dim, hidden_dim // 4),  # GQA (8 KV heads)
            ("V_Projection", M, hidden_dim, hidden_dim // 4),  # GQA (8 KV heads)
            ("Attention_Out", M, hidden_dim, hidden_dim),
            ("SwiGLU_Gate_Up", M, hidden_dim, intermediate_dim * 2),
            ("SwiGLU_Down", M, intermediate_dim, hidden_dim),
        ]

        results = []
        for name, m, k, n in layers:
            res = self.profile_layer("LLaMA-3-8B", name, m, k, n, precision=precision)
            results.append(res)

        total_macs = sum(r.total_macs for r in results)
        total_latency_ns = sum(r.sustained_latency_ns for r in results)
        total_energy_uj = sum(r.energy_uj for r in results)
        avg_throughput = (total_macs / (total_latency_ns * 1e-9)) / 1e12

        return {
            "model": "LLaMA-3-8B",
            "precision": precision,
            "batch_size": batch_size,
            "seq_len": seq_len,
            "layers": [asdict(r) for r in results],
            "total_layer_macs": total_macs,
            "total_layer_latency_ns": total_latency_ns,
            "total_layer_energy_uj": total_energy_uj,
            "average_throughput_tmacs": avg_throughput,
            "energy_efficiency_tmacs_w": avg_throughput / self.P_total,
        }

    def benchmark_gpt2_base(self, batch_size: int = 1, seq_len: int = 1, precision: str = "INT8") -> Dict[str, Any]:
        """Profiles a GPT-2 / BERT-Base Transformer Layer (hidden=768, intermediate=3072)."""
        hidden = 768
        intermediate = 3072
        M = batch_size * seq_len

        layers = [
            ("QKV_Combined_Proj", M, hidden, hidden * 3),
            ("Attention_Output", M, hidden, hidden),
            ("MLP_FC1", M, hidden, intermediate),
            ("MLP_FC2", M, intermediate, hidden),
        ]

        results = [self.profile_layer("GPT-2-Base", name, m, k, n, precision=precision) for name, m, k, n in layers]
        total_macs = sum(r.total_macs for r in results)
        total_latency_ns = sum(r.sustained_latency_ns for r in results)
        total_energy_uj = sum(r.energy_uj for r in results)

        return {
            "model": "GPT-2-Base",
            "precision": precision,
            "layers": [asdict(r) for r in results],
            "total_layer_macs": total_macs,
            "total_layer_latency_ns": total_latency_ns,
            "total_layer_energy_uj": total_energy_uj,
            "average_throughput_tmacs": (total_macs / (total_latency_ns * 1e-9)) / 1e12,
            "energy_efficiency_tmacs_w": ((total_macs / (total_latency_ns * 1e-9)) / 1e12) / self.P_total,
        }

    def benchmark_vit_huge(self, batch_size: int = 1, precision: str = "INT8") -> Dict[str, Any]:
        """Profiles a Vision Transformer (ViT-Huge) Layer (hidden=1280, intermediate=5120)."""
        hidden = 1280
        intermediate = 5120
        M = batch_size * 196  # 196 image patches (14x14)

        layers = [
            ("QKV_Projection", M, hidden, hidden * 3),
            ("Proj_Out", M, hidden, hidden),
            ("MLP_Dense1", M, hidden, intermediate),
            ("MLP_Dense2", M, intermediate, hidden),
        ]

        results = [self.profile_layer("ViT-Huge", name, m, k, n, precision=precision) for name, m, k, n in layers]
        total_macs = sum(r.total_macs for r in results)
        total_latency_ns = sum(r.sustained_latency_ns for r in results)
        total_energy_uj = sum(r.energy_uj for r in results)

        return {
            "model": "ViT-Huge",
            "precision": precision,
            "layers": [asdict(r) for r in results],
            "total_layer_macs": total_macs,
            "total_layer_latency_ns": total_latency_ns,
            "total_layer_energy_uj": total_energy_uj,
            "average_throughput_tmacs": (total_macs / (total_latency_ns * 1e-9)) / 1e12,
            "energy_efficiency_tmacs_w": ((total_macs / (total_latency_ns * 1e-9)) / 1e12) / self.P_total,
        }
