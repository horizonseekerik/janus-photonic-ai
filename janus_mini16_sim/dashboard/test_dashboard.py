"""
Automated Pytest Suite for Interactive Visual Dashboard APIs.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from orchestrator.master_orchestrator import JanusMasterOrchestrator
from tier5_python_rns.ai_workload_benchmarks import AIWorkloadProfiler
from tier5_python_rns.batch_token_packer import BatchTokenPacker


def test_dashboard_orchestrator_integration():
    orch = JanusMasterOrchestrator(verbose=False)
    res = orch.evaluate_custom_integer(0xDEADBEEF, print_output=False)
    assert res["is_match"] is True
    assert res["reconstructed"] == 0xDEADBEEF


def test_dashboard_ai_benchmarks_integration():
    profiler = AIWorkloadProfiler()
    res = profiler.benchmark_llama3_8b(batch_size=1, seq_len=1, precision="INT8")
    assert res["model"] == "LLaMA-3-8B"
    assert len(res["layers"]) == 6


def test_dashboard_token_packer_integration():
    packer = BatchTokenPacker()
    attn = packer.pack_multihead_attention(num_heads=32, d_head=128, seq_len=64, precision="INT8")
    assert attn.spatial_row_occupancy_pct == 100.0
    assert attn.bit_exact_match is True
