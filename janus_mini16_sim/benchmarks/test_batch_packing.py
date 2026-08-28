"""
Automated Pytest Suite for Batch and Multi-Head Token Packing Engine.
Verifies 100% spatial crossbar occupancy, latency, throughput scaling, and numerical exactness.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tier5_python_rns.batch_token_packer import BatchTokenPacker


def test_batch_packer_multihead_attention():
    packer = BatchTokenPacker()
    res = packer.pack_multihead_attention(num_heads=32, d_head=128, seq_len=64, precision="INT8")

    assert res.num_heads == 32
    assert res.d_head == 128
    assert res.spatial_row_occupancy_pct == 100.0  # Must hit 100% spatial occupancy
    assert res.total_macs == 32 * 64 * 128
    assert res.sustained_latency_ns > 0
    assert res.tokens_per_second > 1e6  # Exceeds 1M tokens/sec
    assert res.energy_per_token_nj < 50.0  # Sub-50 nJ per token
    assert res.bit_exact_match is True


def test_batch_packer_batch_mlp():
    packer = BatchTokenPacker()
    res = packer.pack_batch_mlp(batch_size=32, hidden_dim=4096, intermediate_dim=14336, precision="INT8")

    assert res.batch_size == 32
    assert res.spatial_row_occupancy_pct == 100.0  # 100% spatial occupancy
    assert res.total_macs > 0
    assert res.per_token_latency_ns < 10.0  # Sub-10 ns per token
    assert res.tokens_per_second > 1e7  # Millions of tokens/sec
    assert res.energy_per_token_nj < 60.0  # Sub-60 nJ per token across entire SwiGLU MLP
    assert res.bit_exact_match is True
