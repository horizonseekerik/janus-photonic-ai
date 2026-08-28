// ==============================================================================
// PROJECT JANUS MINI (16-TILE): JIR FAULT MONITOR
// ==============================================================================
// Monitors terminal StrongARM latch outputs for RRNS parity mismatches.
// Uses a 4-stage pipelined residue generator for RED_M0 (173) and RED_M1 (169)
// to eliminate single-cycle 64-bit modulo operators at 100 GHz.
// Priority-encodes failing channels (5'd1=Compute, 5'd16=Red0, 5'd17=Red1).
// ==============================================================================

`timescale 1ps / 1ps

module jir_fault_monitor (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        in_valid,
    input  wire [63:0] in_reconstructed_X,
    input  wire [7:0]  in_redundant_r0,
    input  wire [7:0]  in_redundant_r1,
    output reg         fault_detected,
    output reg  [4:0]  fault_channel_id
);

    localparam [8:0] RED_M0 = 9'd173;
    localparam [8:0] RED_M1 = 9'd169;

    // Pipelined residue calculation for redundant moduli
    wire       red0_valid;
    wire [7:0] exp_r0;
    wire       red1_valid;
    wire [7:0] exp_r1;

    rns_channel_encoder #(.MOD(RED_M0)) u_enc_red0 (
        .clk(clk),
        .rst_n(rst_n),
        .in_valid(in_valid),
        .in_X(in_reconstructed_X),
        .out_valid(red0_valid),
        .out_r(exp_r0)
    );

    rns_channel_encoder #(.MOD(RED_M1)) u_enc_red1 (
        .clk(clk),
        .rst_n(rst_n),
        .in_valid(in_valid),
        .in_X(in_reconstructed_X),
        .out_valid(red1_valid),
        .out_r(exp_r1)
    );

    // Delay match incoming redundant residues through 4 pipeline stages
    reg [7:0] r0_d1, r0_d2, r0_d3, r0_d4;
    reg [7:0] r1_d1, r1_d2, r1_d3, r1_d4;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r0_d1 <= 8'd0; r0_d2 <= 8'd0; r0_d3 <= 8'd0; r0_d4 <= 8'd0;
            r1_d1 <= 8'd0; r1_d2 <= 8'd0; r1_d3 <= 8'd0; r1_d4 <= 8'd0;
            fault_detected   <= 1'b0;
            fault_channel_id <= 5'd0;
        end else begin
            r0_d1 <= in_redundant_r0;
            r0_d2 <= r0_d1;
            r0_d3 <= r0_d2;
            r0_d4 <= r0_d3;

            r1_d1 <= in_redundant_r1;
            r1_d2 <= r1_d1;
            r1_d3 <= r1_d2;
            r1_d4 <= r1_d3;

            if (red0_valid) begin
                if ((exp_r0 != r0_d4) && (exp_r1 != r1_d4)) begin
                    fault_detected   <= 1'b1;
                    fault_channel_id <= 5'd1;  // Both mismatch: Primary compute tile error
                end else if ((exp_r0 != r0_d4) && (exp_r1 == r1_d4)) begin
                    fault_detected   <= 1'b1;
                    fault_channel_id <= 5'd16; // Redundant Modulus 0 error
                end else if ((exp_r0 == r0_d4) && (exp_r1 != r1_d4)) begin
                    fault_detected   <= 1'b1;
                    fault_channel_id <= 5'd17; // Redundant Modulus 1 error
                end else begin
                    fault_detected   <= 1'b0;
                    fault_channel_id <= 5'd0;  // No fault detected
                end
            end else begin
                fault_detected   <= 1'b0;
                fault_channel_id <= 5'd0;
            end
        end
    end

endmodule
