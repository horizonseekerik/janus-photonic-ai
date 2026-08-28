"""
Automated Pytest & Icarus Verilog Runner for Tier 4 Digital RTL.
Compiles rns_encoder.v, crt_adder_tree.v, jir_fault_monitor.v, and executes tb_crt_adder_tree.v.
"""

import subprocess
import os
import pytest
import shutil

TIER4_DIR = os.path.dirname(os.path.abspath(__file__))
IVERILOG = shutil.which("iverilog") or r"C:\iverilog\bin\iverilog.exe"
VVP = shutil.which("vvp") or r"C:\iverilog\bin\vvp.exe"


def test_iverilog_installation():
    if not os.path.exists(IVERILOG):
        pytest.skip(f"Icarus Verilog compiler not found on PATH or at {IVERILOG}")
    if not os.path.exists(VVP):
        pytest.skip(f"VVP simulation engine not found on PATH or at {VVP}")


def test_rtl_compilation_and_simulation():
    if not os.path.exists(IVERILOG) or not os.path.exists(VVP):
        pytest.skip("Icarus Verilog toolchain is missing")
    vvp_out = os.path.join(TIER4_DIR, "tb_crt.vvp")
    src_files = [
        os.path.join(TIER4_DIR, "rns_encoder.v"),
        os.path.join(TIER4_DIR, "crt_adder_tree.v"),
        os.path.join(TIER4_DIR, "jir_fault_monitor.v"),
        os.path.join(TIER4_DIR, "tb_crt_adder_tree.v"),
    ]

    # Step 1: Compile with iverilog
    compile_cmd = [IVERILOG, "-g2012", "-o", vvp_out] + src_files
    comp_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert comp_res.returncode == 0, f"Compilation failed:\n{comp_res.stderr}"

    # Step 2: Execute with vvp
    sim_res = subprocess.run([VVP, vvp_out], capture_output=True, text=True)
    assert sim_res.returncode == 0, f"Simulation runtime error:\n{sim_res.stderr}"
    assert "[PASS]" in sim_res.stdout, f"Verification failed:\n{sim_res.stdout}"
    assert "Errors=0" in sim_res.stdout, f"Encountered RTL errors:\n{sim_res.stdout}"

    print("\n" + sim_res.stdout)


if __name__ == "__main__":
    test_rtl_compilation_and_simulation()
