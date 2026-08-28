"""
Automated Pytest Suite for AI Workload Profiler and GPU Comparator.
Verifies LLaMA-3-8B, GPT-2, ViT-Huge layer calculations and GPU advantage formulas.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tier5_python_rns.ai_workload_benchmarks import AIWorkloadProfiler
from tier5_python_rns.gpu_comparator import GPUComparator


def test_ai_workload_profiler_llama3():
    profiler = AIWorkloadProfiler()
    res = profiler.benchmark_llama3_8b(batch_size=1, seq_len=1, precision="INT8")

    assert res["model"] == "LLaMA-3-8B"
    assert res["total_layer_macs"] > 0
    assert res["total_layer_latency_ns"] > 0
    assert res["total_layer_energy_uj"] > 0
    assert res["average_throughput_tmacs"] > 100.0  # Must exceed 100 TMAC/s
    assert res["energy_efficiency_tmacs_w"] > 50.0  # Must exceed 50 TMAC/s/W
    for layer in res["layers"]:
        assert layer["bit_exact_verified"] is True


def test_ai_workload_profiler_gpt2():
    profiler = AIWorkloadProfiler()
    res = profiler.benchmark_gpt2_base(batch_size=1, seq_len=1, precision="INT8")

    assert res["model"] == "GPT-2-Base"
    assert len(res["layers"]) == 4
    assert res["total_layer_macs"] > 0
    for layer in res["layers"]:
        assert layer["bit_exact_verified"] is True


def test_ai_workload_profiler_vit():
    profiler = AIWorkloadProfiler()
    res = profiler.benchmark_vit_huge(batch_size=1, precision="INT8")

    assert res["model"] == "ViT-Huge"
    assert len(res["layers"]) == 4
    assert res["total_layer_macs"] > 0
    for layer in res["layers"]:
        assert layer["bit_exact_verified"] is True


def test_gpu_comparator_metrics():
    comparator = GPUComparator()
    hw_table = comparator.get_hardware_comparison_table()

    # Verify JANUS efficiency advantage is > 50x over modern GPUs
    assert hw_table["janus_vs_h100_energy_efficiency_mult"] >= 100.0
    assert hw_table["janus_vs_b200_energy_efficiency_mult"] >= 50.0

    # Verify compute area density advantage
    assert hw_table["janus_vs_h100_density_mult"] >= 5.0
    assert hw_table["janus_vs_b200_density_mult"] >= 5.0

    # Verify LLaMA-3 comparison
    llama_comp = comparator.compare_llama3_layer("INT8")
    assert llama_comp["energy_savings_vs_h100"] > 50.0
    assert llama_comp["energy_savings_vs_b200"] > 30.0
