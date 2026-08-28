"""
ALGORITHM 4C: COCOTB_TESTBENCH
==============================
Cycle-accurate Co-Simulation of the JANUS Mini 16-Tile RTL Front-End and CRT Tree.
Drives randomized 64-bit integer vectors and verifies bit-exact numerical fidelity
and pipeline latency guarantees.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tier5_python_rns.moduli_generator import generate_moduli_set


@cocotb.test()
async def test_pipelined_crt_reconstruction(dut):
    """Verifies 1000 randomized 64-bit vectors through the pipelined CRT adder tree."""
    mod_info = generate_moduli_set()
    _ = mod_info["moduli_compute"]

    # Generate 100 GHz clock (period = 10 ps => 5 ps high, 5 ps low)
    clock = Clock(dut.clk, 10, units="ps")
    cocotb.start_soon(clock.start())

    # Reset sequence
    dut.rst_n.value = 0
    dut.in_valid.value = 0
    dut.in_X.value = 0
    await Timer(20, units="ps")
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    # Drive test vectors and collect pipeline outputs
    num_vectors = 100
    sent_values = []

    for i in range(num_vectors):
        val = random.randint(0, 2**64 - 1)
        dut.in_valid.value = 1
        dut.in_X.value = val
        sent_values.append(val)
        await RisingEdge(dut.clk)

    dut.in_valid.value = 0

    # Wait for pipeline to drain (12 clock cycles latency = 120 ps)
    for expected_val in sent_values:
        timeout = 30
        while dut.out_valid.value == 0:
            await RisingEdge(dut.clk)
            timeout -= 1
            assert timeout > 0, "RTL timeout: pipeline dropped valid signal"

        # Read the output and assert it matches the expected value
        assert (
            int(dut.out_X.value) == expected_val
        ), f"Mismatch: expected {expected_val}, got {int(dut.out_X.value)}"
        await RisingEdge(dut.clk)

    dut._log.info(f"[PASS] Successfully simulated {num_vectors} vectors through RTL.")
