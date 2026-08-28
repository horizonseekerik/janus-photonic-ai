"""
PROJECT JANUS MINI (16-TILE): RTL SYNTHESIS & STANDARD-CELL AREA ANALYZER
==========================================================================
Performs structural cell mapping, Gate Equivalent (GE) counting, standard-cell
die area estimation, and power budgeting for the Tier 4 100 GHz Digital RTL blocks:
  1. crt_adder_tree.v (8-stage wave-pipelined CRT reconstruction tree)
  2. rns_encoder.v (4-stage byte-decomposed residue encoder)
  3. jir_fault_monitor.v (pipelined RRNS parity violation detector)

Estimates area across standard semiconductor process nodes:
  - TSMC 7nm FinFET (0.065 um^2 / NAND2 Gate Equivalent)
  - GF 12nm FinFET  (0.120 um^2 / NAND2 Gate Equivalent)
  - 28nm FD-SOI     (0.500 um^2 / NAND2 Gate Equivalent)
"""

import sys
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from configs import mini_16t_constants as cfg


@dataclass
class ModuleSynthesisReport:
    module_name: str
    pipeline_stages: int
    num_dff_bits: int
    num_mux_bits: int
    num_adder_bits: int
    num_logic_gates: int
    total_gate_equivalents_ge: int
    area_7nm_um2: float
    area_12nm_um2: float
    area_28nm_um2: float
    dynamic_power_mw_100ghz: float


# Process Node Constants
NAND2_AREA_7NM = 0.065   # um^2 per GE
NAND2_AREA_12NM = 0.120  # um^2 per GE
NAND2_AREA_28NM = 0.500  # um^2 per GE

# Gate Equivalent Weights (NAND2 = 1.0 GE)
GE_PER_DFF_BIT = 6.0     # D-Flip-Flop with async reset ~ 6.0 GE
GE_PER_MUX_BIT = 3.0     # 2:1 MUX ~ 3.0 GE
GE_PER_ADDER_BIT = 8.0   # Full Adder cell ~ 8.0 GE / Half Adder ~ 4.0 GE
GE_PER_LOGIC_GATE = 1.5  # Average 2-input logic gate ~ 1.5 GE


class RTLSynthesisAnalyzer:
    """Analyzes and estimates synthesis gate count and silicon area for Tier 4 RTL."""

    def __init__(self):
        self.f_clk = cfg.f_clk  # 100 GHz

    def analyze_crt_adder_tree(self) -> ModuleSynthesisReport:
        """
        Analyzes crt_adder_tree.v (8 pipeline stages):
          - Stage 1: 16 parallel 256-entry x 136-bit ROM LUTs (synthesized standard-cell MUX trees)
          - Stages 2-5: 16-to-8, 8-to-4, 4-to-2, 2-to-1 pipelined binary adder trees
          - Stages 6-8: Modular projection and 64-bit output register latch
        """
        # Pipeline Registers (DFFs)
        # Stage 1: 16 x 136 = 2,176 bits
        # Stage 2: 8 x 137  = 1,096 bits
        # Stage 3: 4 x 138  = 552 bits
        # Stage 4: 2 x 139  = 278 bits
        # Stage 5: 1 x 140  = 140 bits
        # Stage 6: 1 x 136  = 136 bits
        # Stage 7: 1 x 65   = 65 bits
        # Stage 8: 1 x 64   = 64 bits (output)
        # Control flags: ~10 bits
        num_dff = 2176 + 1096 + 552 + 278 + 140 + 136 + 65 + 64 + 10  # ~4,517 DFFs

        # Stage 1 ROM LUT standard-cell MUX logic:
        # 16 channels x 256 entries x 136 bits.
        # Synthesized into 8:1 MUX trees per bit: ~16 x 136 x (31 gates) ~ 67,456 logic gates
        num_mux_bits = 16 * 136 * 8
        num_adder_bits = (8 * 137) + (4 * 138) + (2 * 139) + (1 * 140) + 136  # ~2,202 adder bits
        num_logic = 67456 + 2500

        total_ge = int(
            (num_dff * GE_PER_DFF_BIT)
            + (num_adder_bits * GE_PER_ADDER_BIT)
            + (num_logic * GE_PER_LOGIC_GATE)
        )

        area_7nm = total_ge * NAND2_AREA_7NM
        area_12nm = total_ge * NAND2_AREA_12NM
        area_28nm = total_ge * NAND2_AREA_28NM

        # Dynamic power at 100 GHz (C_eff * Vdd^2 * f)
        # Approx 1.05 W per chip across all active CRT trees
        power_mw = 1050.0

        return ModuleSynthesisReport(
            module_name="crt_adder_tree.v",
            pipeline_stages=8,
            num_dff_bits=num_dff,
            num_mux_bits=num_mux_bits,
            num_adder_bits=num_adder_bits,
            num_logic_gates=num_logic,
            total_gate_equivalents_ge=total_ge,
            area_7nm_um2=area_7nm,
            area_12nm_um2=area_12nm,
            area_28nm_um2=area_28nm,
            dynamic_power_mw_100ghz=power_mw,
        )

    def analyze_rns_encoder(self) -> ModuleSynthesisReport:
        """
        Analyzes rns_encoder.v (4 pipeline stages):
          - 16 parallel residue channels
          - 8 byte decomposition multipliers & 3-stage adder tree per channel
        """
        # DFF bits:
        # Stage 1: 16 channels x 8 bytes x 8 bits = 1,024 bits
        # Stage 2: 16 channels x 4 adders x 9 bits = 576 bits
        # Stage 3: 16 channels x 2 adders x 10 bits = 320 bits
        # Stage 4: 16 channels x 8 bits (output) = 128 bits
        num_dff = 1024 + 576 + 320 + 128 + 16  # ~2,064 DFFs

        num_adder_bits = 16 * ((4 * 9) + (2 * 10) + (1 * 10))  # ~1,056 adder bits
        num_logic = 16 * 8 * 32  # ~4,096 logic gates for constants & Barrett reductions

        total_ge = int(
            (num_dff * GE_PER_DFF_BIT)
            + (num_adder_bits * GE_PER_ADDER_BIT)
            + (num_logic * GE_PER_LOGIC_GATE)
        )

        return ModuleSynthesisReport(
            module_name="rns_encoder.v",
            pipeline_stages=4,
            num_dff_bits=num_dff,
            num_mux_bits=512,
            num_adder_bits=num_adder_bits,
            num_logic_gates=num_logic,
            total_gate_equivalents_ge=total_ge,
            area_7nm_um2=total_ge * NAND2_AREA_7NM,
            area_12nm_um2=total_ge * NAND2_AREA_12NM,
            area_28nm_um2=total_ge * NAND2_AREA_28NM,
            dynamic_power_mw_100ghz=420.0,
        )

    def analyze_jir_fault_monitor(self) -> ModuleSynthesisReport:
        """Analyzes jir_fault_monitor.v (4 pipeline stages)."""
        num_dff = 2 * (64 + 32 + 16 + 8) + 16  # ~256 DFFs
        num_adder_bits = 2 * 64
        num_logic = 1200  # Priority encoder & syndrome comparison

        total_ge = int(
            (num_dff * GE_PER_DFF_BIT)
            + (num_adder_bits * GE_PER_ADDER_BIT)
            + (num_logic * GE_PER_LOGIC_GATE)
        )

        return ModuleSynthesisReport(
            module_name="jir_fault_monitor.v",
            pipeline_stages=4,
            num_dff_bits=num_dff,
            num_mux_bits=64,
            num_adder_bits=num_adder_bits,
            num_logic_gates=num_logic,
            total_gate_equivalents_ge=total_ge,
            area_7nm_um2=total_ge * NAND2_AREA_7NM,
            area_12nm_um2=total_ge * NAND2_AREA_12NM,
            area_28nm_um2=total_ge * NAND2_AREA_28NM,
            dynamic_power_mw_100ghz=120.0,
        )

    def get_full_chip_digital_synthesis_summary(self) -> Dict[str, Any]:
        """Returns consolidated digital synthesis metrics across all Tier 4 blocks."""
        crt_rep = self.analyze_crt_adder_tree()
        enc_rep = self.analyze_rns_encoder()
        jir_rep = self.analyze_jir_fault_monitor()

        total_ge = crt_rep.total_gate_equivalents_ge + enc_rep.total_gate_equivalents_ge + jir_rep.total_gate_equivalents_ge
        total_area_7nm_mm2 = (crt_rep.area_7nm_um2 + enc_rep.area_7nm_um2 + jir_rep.area_7nm_um2) / 1e6
        total_area_12nm_mm2 = (crt_rep.area_12nm_um2 + enc_rep.area_12nm_um2 + jir_rep.area_12nm_um2) / 1e6
        total_area_28nm_mm2 = (crt_rep.area_28nm_um2 + enc_rep.area_28nm_um2 + jir_rep.area_28nm_um2) / 1e6

        return {
            "modules": [asdict(crt_rep), asdict(enc_rep), asdict(jir_rep)],
            "total_digital_ge": total_ge,
            "total_area_7nm_mm2": total_area_7nm_mm2,
            "total_area_12nm_mm2": total_area_12nm_mm2,
            "total_area_28nm_mm2": total_area_28nm_mm2,
            "total_cmos_substrate_budget_mm2": 50.0,
            "area_occupancy_7nm_pct": (total_area_7nm_mm2 / 50.0) * 100.0,
            "area_occupancy_12nm_pct": (total_area_12nm_mm2 / 50.0) * 100.0,
        }

    def print_synthesis_report(self):
        summary = self.get_full_chip_digital_synthesis_summary()

        print("\n" + "=" * 96)
        print("  PROJECT JANUS: TIER 4 DIGITAL RTL SYNTHESIS & STANDARD-CELL AREA BREAKDOWN")
        print("=" * 96)
        print(f"{'Module Name':<20} | {'Stages':<6} | {'DFF Bits':<10} | {'Total GE':<12} | {'Area @ 7nm':<14} | {'Area @ 12nm':<14}")
        print("-" * 96)

        for m in summary["modules"]:
            area_7 = f"{m['area_7nm_um2'] / 1e3:.1f} k um²"
            area_12 = f"{m['area_12nm_um2'] / 1e3:.1f} k um²"
            print(f"{m['module_name'][:20]:<20} | {m['pipeline_stages']:<6} | {m['num_dff_bits']:<10} | {m['total_gate_equivalents_ge']:<12,d} | {area_7:<14} | {area_12:<14}")

        print("-" * 96)
        print(f"  TOTAL DIGITAL CORE: {summary['total_digital_ge']:,} Gate Equivalents (GE)")
        print(f"  Total Area @ 7nm FinFET : {summary['total_area_7nm_mm2']:.4f} mm² ({summary['area_occupancy_7nm_pct']:.2f}% of 50 mm² CMOS die)")
        print(f"  Total Area @ 12nm FinFET: {summary['total_area_12nm_mm2']:.4f} mm² ({summary['area_occupancy_12nm_pct']:.2f}% of 50 mm² CMOS die)")
        print("=" * 96 + "\n")


if __name__ == "__main__":
    analyzer = RTLSynthesisAnalyzer()
    analyzer.print_synthesis_report()
