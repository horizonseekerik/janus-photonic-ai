"""
Automated Pytest Suite for RTL Synthesis and Standard-Cell Area Analyzer.
Verifies gate counts, area scaling across process nodes, and synthesis script presence.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tier4_rtl_digital.rtl_synthesis_analyzer import RTLSynthesisAnalyzer


def test_crt_adder_tree_synthesis_report():
    analyzer = RTLSynthesisAnalyzer()
    res = analyzer.analyze_crt_adder_tree()

    assert res.module_name == "crt_adder_tree.v"
    assert res.pipeline_stages == 8
    assert res.num_dff_bits > 4000
    assert res.total_gate_equivalents_ge > 50000
    assert res.area_7nm_um2 < 20000.0  # Sub-20k um^2 at 7nm
    assert res.dynamic_power_mw_100ghz <= 1200.0


def test_rns_encoder_synthesis_report():
    analyzer = RTLSynthesisAnalyzer()
    res = analyzer.analyze_rns_encoder()

    assert res.module_name == "rns_encoder.v"
    assert res.pipeline_stages == 4
    assert res.num_dff_bits > 1500
    assert res.total_gate_equivalents_ge > 10000
    assert res.area_7nm_um2 < 10000.0


def test_full_chip_synthesis_summary():
    analyzer = RTLSynthesisAnalyzer()
    summary = analyzer.get_full_chip_digital_synthesis_summary()

    assert summary["total_digital_ge"] > 80000
    assert summary["total_area_7nm_mm2"] < 0.1  # Fits in < 0.1 mm^2
    assert summary["area_occupancy_7nm_pct"] < 1.0  # < 1% of the 50 mm^2 CMOS substrate

    # Check synth.ys presence
    synth_ys_path = os.path.join(BASE_DIR, "tier4_rtl_digital", "synth.ys")
    assert os.path.exists(synth_ys_path)
