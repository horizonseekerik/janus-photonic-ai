#!/usr/bin/env python3
"""
PROJECT JANUS MINI (16-TILE): MASTER CO-SIMULATION RUNNER
==========================================================
Top-level entrypoint script to execute the full multi-physics co-simulation pipeline,
individual simulation tiers, or evaluate custom numbers & multiplications through the
16-tile spatial RNS optical/CMOS pipeline.

Usage:
    python run_mini16_full_cosim.py --verbose
    python run_mini16_full_cosim.py --tier 1
    python run_mini16_full_cosim.py --val 123456789012345678
    python run_mini16_full_cosim.py --val 0xDEADBEEFCAFEBABE
    python run_mini16_full_cosim.py --mult 123456789 987654321
    python run_mini16_full_cosim.py --interactive
"""

import sys
import os
import argparse

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from orchestrator.master_orchestrator import JanusMasterOrchestrator


def parse_custom_int(val_str: str) -> int:
    """Parses integer in decimal or hexadecimal format."""
    val_str = val_str.strip()
    if val_str.lower().startswith("0x"):
        return int(val_str, 16)
    return int(val_str)


def run_interactive_mode(orchestrator: JanusMasterOrchestrator):
    """Interactive CLI to evaluate custom numbers through the RNS/CRT pipeline."""
    print("\n" + "=" * 80)
    print("  PROJECT JANUS MINI (16-TILE): INTERACTIVE CUSTOM INPUT EVALUATOR")
    print("=" * 80)
    print("  Commands:")
    print("    eval <int or hex>       : Decompose into 16 RNS channels & reconstruct via CRT")
    print("    mult <int_a> <int_b>    : Multiply two integers across 16 optical residue tiles")
    print("    exit / quit             : Exit interactive mode")
    print("=" * 80 + "\n")

    while True:
        try:
            line = input("JANUS-RNS> ").strip()
            if not line:
                continue
            if line.lower() in ["exit", "quit", "q"]:
                print("Exiting interactive mode.")
                break

            parts = line.split()
            cmd = parts[0].lower()

            if cmd == "eval" and len(parts) >= 2:
                val = parse_custom_int(parts[1])
                orchestrator.evaluate_custom_integer(val, print_output=True)
            elif cmd == "mult" and len(parts) >= 3:
                a = parse_custom_int(parts[1])
                b = parse_custom_int(parts[2])
                orchestrator.evaluate_custom_multiply(a, b, print_output=True)
            elif cmd.isdigit() or (cmd.startswith("0x") and len(parts) == 1):
                val = parse_custom_int(cmd)
                orchestrator.evaluate_custom_integer(val, print_output=True)
            else:
                print(f"Unknown command: '{line}'. Usage: 'eval <val>' or 'mult <a> <b>'")
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Project JANUS Mini 16-Tile: End-to-End Co-Simulation Master Runner"
    )
    parser.add_argument(
        "--tier",
        type=str,
        default=None,
        choices=["1", "2", "3", "4", "5", "all"],
        help="Simulation tier to execute (1-5 or 'all' for full co-simulation)",
    )
    parser.add_argument(
        "--val",
        type=str,
        default=None,
        help="Evaluate a custom 64-bit integer (decimal or hex e.g. 0x123456789ABCDEF0)",
    )
    parser.add_argument(
        "--mult",
        nargs=2,
        type=str,
        default=None,
        metavar=("A", "B"),
        help="Multiply two custom numbers A and B across the 16-tile spatial RNS engine",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        default=False,
        help="Launch interactive REPL mode for custom number evaluation",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable detailed verbose output for all simulation steps",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save generated artifacts and reports",
    )
    parser.add_argument(
        "--report",
        type=str,
        default=None,
        help="Custom destination filepath for the markdown verification report",
    )

    args = parser.parse_args()

    orchestrator = JanusMasterOrchestrator(
        verbose=args.verbose, output_dir=args.output_dir
    )

    # 1. Custom Single Value
    if args.val is not None:
        val = parse_custom_int(args.val)
        res = orchestrator.evaluate_custom_integer(val, print_output=True)
        sys.exit(0 if res["is_match"] else 1)

    # 2. Custom Multiplication
    if args.mult is not None:
        a = parse_custom_int(args.mult[0])
        b = parse_custom_int(args.mult[1])
        res = orchestrator.evaluate_custom_multiply(a, b, print_output=True)
        sys.exit(0 if res["is_match"] else 1)

    # 3. Interactive Mode
    if args.interactive:
        run_interactive_mode(orchestrator)
        sys.exit(0)

    # 4. Standard Tier / Full Co-Sim Execution
    tier_choice = args.tier or "all"
    if tier_choice == "all":
        results = orchestrator.run_full_cosim()
        if args.report and os.path.exists(results["report_path"]):
            import shutil

            shutil.copy(results["report_path"], args.report)
            print(f"Report copied to: {args.report}")
        sys.exit(0 if results["overall_pass"] else 1)
    else:
        tier_num = int(tier_choice)
        print(f"Running individual Tier {tier_num} simulation...")
        orchestrator.validate_global_constants()
        if tier_num == 1:
            res = orchestrator.run_tier1_optics()
        elif tier_num == 2:
            res = orchestrator.run_tier2_thermal()
        elif tier_num == 3:
            orchestrator.run_tier1_optics()
            res = orchestrator.run_tier3_circuit()
        elif tier_num == 4:
            res = orchestrator.run_tier4_rtl()
        elif tier_num == 5:
            orchestrator.run_tier2_thermal()
            orchestrator.run_tier3_circuit()
            res = orchestrator.run_tier5_algorithms()
        print(f"Tier {tier_num} execution completed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
