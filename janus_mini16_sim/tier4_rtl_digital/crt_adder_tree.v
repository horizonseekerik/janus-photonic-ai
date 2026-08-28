// ==============================================================================
// PROJECT JANUS MINI (16-TILE): PIPELINED CRT ADDER TREE (ALGORITHM 4B)
// ==============================================================================
// Reconstructs 64-bit integer X from 16 residue channels using an 8-stage pipeline.
// Latency: 8 clock cycles (80 ps @ 100 GHz), Gate-level accumulation delay per stage <= 10 ps.
// ==============================================================================

`timescale 1ps / 1ps

module crt_adder_tree (
    input  wire         clk,
    input  wire         rst_n,
    input  wire         in_valid,
    input  wire [7:0]   in_r0,
    input  wire [7:0]   in_r1,
    input  wire [7:0]   in_r2,
    input  wire [7:0]   in_r3,
    input  wire [7:0]   in_r4,
    input  wire [7:0]   in_r5,
    input  wire [7:0]   in_r6,
    input  wire [7:0]   in_r7,
    input  wire [7:0]   in_r8,
    input  wire [7:0]   in_r9,
    input  wire [7:0]   in_r10,
    input  wire [7:0]   in_r11,
    input  wire [7:0]   in_r12,
    input  wire [7:0]   in_r13,
    input  wire [7:0]   in_r14,
    input  wire [7:0]   in_r15,
    output reg          out_valid,
    output reg  [63:0]  out_X
);

    // Total Dynamic Range Modulus (Hexadecimal 128-bit)
    localparam [127:0] M_TOTAL    = 128'h120de925ab00c09fd76326e49e93bf00;
    localparam [139:0] M_TOTAL_X8 = {9'b0,  M_TOTAL, 3'b000}; // 8 * M_TOTAL
    localparam [139:0] M_TOTAL_X4 = {10'b0, M_TOTAL, 2'b00};  // 4 * M_TOTAL
    localparam [139:0] M_TOTAL_X2 = {11'b0, M_TOTAL, 1'b0};   // 2 * M_TOTAL
    localparam [139:0] M_TOTAL_X1 = {12'b0, M_TOTAL};         // 1 * M_TOTAL

    // Precomputed CRT Constants (M_i, N_i, m_i)
    localparam [8:0]   M_0 = 9'd256;
    localparam [8:0]   N_0 = 9'd63;
    localparam [127:0] MI_0 = 128'h120de925ab00c09fd76326e49e93bf;
    localparam [8:0]   M_1 = 9'd251;
    localparam [8:0]   N_1 = 9'd237;
    localparam [127:0] MI_1 = 128'h1269fb0ceb9ac6805920cadae50d00;
    localparam [8:0]   M_2 = 9'd243;
    localparam [8:0]   N_2 = 9'd236;
    localparam [127:0] MI_2 = 128'h13052c66e49cb5dc03918af2f50500;
    localparam [8:0]   M_3 = 9'd241;
    localparam [8:0]   N_3 = 9'd79;
    localparam [127:0] MI_3 = 128'h132d94deb7c55054cf8c608cdfaf00;
    localparam [8:0]   M_4 = 9'd239;
    localparam [8:0]   N_4 = 9'd81;
    localparam [127:0] MI_4 = 128'h1356aa779c6359929328dd9bfa3100;
    localparam [8:0]   M_5 = 9'd233;
    localparam [8:0]   N_5 = 9'd168;
    localparam [127:0] MI_5 = 128'h13d6269dd98c5cfa5506c25ac66700;
    localparam [8:0]   M_6 = 9'd229;
    localparam [8:0]   N_6 = 9'd50;
    localparam [127:0] MI_6 = 128'h142eda27df9585ba833a4d040bd300;
    localparam [8:0]   M_7 = 9'd227;
    localparam [8:0]   N_7 = 9'd18;
    localparam [127:0] MI_7 = 128'h145c6006645f947098aef91ce47500;
    localparam [8:0]   M_8 = 9'd223;
    localparam [8:0]   N_8 = 9'd59;
    localparam [127:0] MI_8 = 128'h14b9dee09f92a85278fb951d692100;
    localparam [8:0]   M_9 = 9'd211;
    localparam [8:0]   N_9 = 9'd74;
    localparam [127:0] MI_9 = 128'h15e7a05486ad32806a06402c6de500;
    localparam [8:0]   M_10 = 9'd199;
    localparam [8:0]   N_10 = 9'd31;
    localparam [127:0] MI_10 = 128'h1739c64cc2414a213e3f3b09cd4900;
    localparam [8:0]   M_11 = 9'd197;
    localparam [8:0]   N_11 = 9'd27;
    localparam [127:0] MI_11 = 128'h177623470a665693ef9c22f282b300;
    localparam [8:0]   M_12 = 9'd193;
    localparam [8:0]   N_12 = 9'd172;
    localparam [127:0] MI_12 = 128'h17f29e0a2bc6a2a6eb4a7b37347f00;
    localparam [8:0]   M_13 = 9'd191;
    localparam [8:0]   N_13 = 9'd154;
    localparam [127:0] MI_13 = 128'h1832cff226df802aad6b6dc32d0100;
    localparam [8:0]   M_14 = 9'd181;
    localparam [8:0]   N_14 = 9'd90;
    localparam [127:0] MI_14 = 128'h1989112e3455ed14fdb815106f2300;
    localparam [8:0]   M_15 = 9'd179;
    localparam [8:0]   N_15 = 9'd9;
    localparam [127:0] MI_15 = 128'h19d21b6234eb9fa43e0d16bacec500;

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 1: Precomputed Partial Product LUTs (ROMs)
    // pp[i] = ((r[i] * N[i]) mod m[i]) * MI_i
    // --------------------------------------------------------------------------
    reg [135:0] lut_pp0  [0:255];
    reg [135:0] lut_pp1  [0:255];
    reg [135:0] lut_pp2  [0:255];
    reg [135:0] lut_pp3  [0:255];
    reg [135:0] lut_pp4  [0:255];
    reg [135:0] lut_pp5  [0:255];
    reg [135:0] lut_pp6  [0:255];
    reg [135:0] lut_pp7  [0:255];
    reg [135:0] lut_pp8  [0:255];
    reg [135:0] lut_pp9  [0:255];
    reg [135:0] lut_pp10 [0:255];
    reg [135:0] lut_pp11 [0:255];
    reg [135:0] lut_pp12 [0:255];
    reg [135:0] lut_pp13 [0:255];
    reg [135:0] lut_pp14 [0:255];
    reg [135:0] lut_pp15 [0:255];

    integer idx;
    initial begin
        for (idx = 0; idx < 256; idx = idx + 1) begin
            lut_pp0[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_0})  % {7'b0, M_0})  * MI_0;
            lut_pp1[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_1})  % {7'b0, M_1})  * MI_1;
            lut_pp2[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_2})  % {7'b0, M_2})  * MI_2;
            lut_pp3[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_3})  % {7'b0, M_3})  * MI_3;
            lut_pp4[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_4})  % {7'b0, M_4})  * MI_4;
            lut_pp5[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_5})  % {7'b0, M_5})  * MI_5;
            lut_pp6[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_6})  % {7'b0, M_6})  * MI_6;
            lut_pp7[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_7})  % {7'b0, M_7})  * MI_7;
            lut_pp8[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_8})  % {7'b0, M_8})  * MI_8;
            lut_pp9[idx]  = (({8'b0, idx[7:0]} * {7'b0, N_9})  % {7'b0, M_9})  * MI_9;
            lut_pp10[idx] = (({8'b0, idx[7:0]} * {7'b0, N_10}) % {7'b0, M_10}) * MI_10;
            lut_pp11[idx] = (({8'b0, idx[7:0]} * {7'b0, N_11}) % {7'b0, M_11}) * MI_11;
            lut_pp12[idx] = (({8'b0, idx[7:0]} * {7'b0, N_12}) % {7'b0, M_12}) * MI_12;
            lut_pp13[idx] = (({8'b0, idx[7:0]} * {7'b0, N_13}) % {7'b0, M_13}) * MI_13;
            lut_pp14[idx] = (({8'b0, idx[7:0]} * {7'b0, N_14}) % {7'b0, M_14}) * MI_14;
            lut_pp15[idx] = (({8'b0, idx[7:0]} * {7'b0, N_15}) % {7'b0, M_15}) * MI_15;
        end
    end

    reg         st1_valid;
    reg [135:0] st1_pp0,  st1_pp1,  st1_pp2,  st1_pp3;
    reg [135:0] st1_pp4,  st1_pp5,  st1_pp6,  st1_pp7;
    reg [135:0] st1_pp8,  st1_pp9,  st1_pp10, st1_pp11;
    reg [135:0] st1_pp12, st1_pp13, st1_pp14, st1_pp15;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st1_valid <= 1'b0;
            st1_pp0  <= 136'd0; st1_pp1  <= 136'd0; st1_pp2  <= 136'd0; st1_pp3  <= 136'd0;
            st1_pp4  <= 136'd0; st1_pp5  <= 136'd0; st1_pp6  <= 136'd0; st1_pp7  <= 136'd0;
            st1_pp8  <= 136'd0; st1_pp9  <= 136'd0; st1_pp10 <= 136'd0; st1_pp11 <= 136'd0;
            st1_pp12 <= 136'd0; st1_pp13 <= 136'd0; st1_pp14 <= 136'd0; st1_pp15 <= 136'd0;
        end else begin
            st1_valid <= in_valid;
            if (in_valid) begin
                st1_pp0  <= lut_pp0[in_r0];
                st1_pp1  <= lut_pp1[in_r1];
                st1_pp2  <= lut_pp2[in_r2];
                st1_pp3  <= lut_pp3[in_r3];
                st1_pp4  <= lut_pp4[in_r4];
                st1_pp5  <= lut_pp5[in_r5];
                st1_pp6  <= lut_pp6[in_r6];
                st1_pp7  <= lut_pp7[in_r7];
                st1_pp8  <= lut_pp8[in_r8];
                st1_pp9  <= lut_pp9[in_r9];
                st1_pp10 <= lut_pp10[in_r10];
                st1_pp11 <= lut_pp11[in_r11];
                st1_pp12 <= lut_pp12[in_r12];
                st1_pp13 <= lut_pp13[in_r13];
                st1_pp14 <= lut_pp14[in_r14];
                st1_pp15 <= lut_pp15[in_r15];
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 2: Pairwise Addition (16 -> 8 Adders)
    // --------------------------------------------------------------------------
    reg         st2_valid;
    reg [136:0] st2_s0, st2_s1, st2_s2, st2_s3;
    reg [136:0] st2_s4, st2_s5, st2_s6, st2_s7;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st2_valid <= 1'b0;
            st2_s0 <= 137'd0; st2_s1 <= 137'd0; st2_s2 <= 137'd0; st2_s3 <= 137'd0;
            st2_s4 <= 137'd0; st2_s5 <= 137'd0; st2_s6 <= 137'd0; st2_s7 <= 137'd0;
        end else begin
            st2_valid <= st1_valid;
            if (st1_valid) begin
                st2_s0 <= st1_pp0  + st1_pp1;
                st2_s1 <= st1_pp2  + st1_pp3;
                st2_s2 <= st1_pp4  + st1_pp5;
                st2_s3 <= st1_pp6  + st1_pp7;
                st2_s4 <= st1_pp8  + st1_pp9;
                st2_s5 <= st1_pp10 + st1_pp11;
                st2_s6 <= st1_pp12 + st1_pp13;
                st2_s7 <= st1_pp14 + st1_pp15;
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 3: Quad-wise Addition (8 -> 4 Adders)
    // --------------------------------------------------------------------------
    reg         st3_valid;
    reg [137:0] st3_s0, st3_s1, st3_s2, st3_s3;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st3_valid <= 1'b0;
            st3_s0 <= 138'd0; st3_s1 <= 138'd0; st3_s2 <= 138'd0; st3_s3 <= 138'd0;
        end else begin
            st3_valid <= st2_valid;
            if (st2_valid) begin
                st3_s0 <= st2_s0 + st2_s1;
                st3_s1 <= st2_s2 + st2_s3;
                st3_s2 <= st2_s4 + st2_s5;
                st3_s3 <= st2_s6 + st2_s7;
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 4: Dual-wise Addition (4 -> 2 Adders) [Registered Split]
    // --------------------------------------------------------------------------
    reg         st4_valid;
    reg [138:0] st4_s0, st4_s1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st4_valid <= 1'b0;
            st4_s0    <= 139'd0;
            st4_s1    <= 139'd0;
        end else begin
            st4_valid <= st3_valid;
            if (st3_valid) begin
                st4_s0 <= st3_s0 + st3_s1;
                st4_s1 <= st3_s2 + st3_s3;
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 5: Final Accumulation (2 -> 1) & Modulo Reduction (Step 1: 8*M)
    // --------------------------------------------------------------------------
    reg         st5_valid;
    reg [139:0] st5_val;
    wire [139:0] raw_sum = {1'b0, st4_s0} + {1'b0, st4_s1};
    wire [139:0] sub8    = raw_sum - M_TOTAL_X8;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st5_valid <= 1'b0;
            st5_val   <= 140'd0;
        end else begin
            st5_valid <= st4_valid;
            if (st4_valid) begin
                st5_val <= (raw_sum >= M_TOTAL_X8) ? sub8 : raw_sum;
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 6: Modulo Reduction (Step 2: 4*M)
    // --------------------------------------------------------------------------
    reg         st6_valid;
    reg [139:0] st6_val;
    wire [139:0] sub4 = st5_val - M_TOTAL_X4;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st6_valid <= 1'b0;
            st6_val   <= 140'd0;
        end else begin
            st6_valid <= st5_valid;
            if (st5_valid) begin
                st6_val <= (st5_val >= M_TOTAL_X4) ? sub4 : st5_val;
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 7: Modulo Reduction (Step 3: 2*M)
    // --------------------------------------------------------------------------
    reg         st7_valid;
    reg [139:0] st7_val;
    wire [139:0] sub2 = st6_val - M_TOTAL_X2;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st7_valid <= 1'b0;
            st7_val   <= 140'd0;
        end else begin
            st7_valid <= st6_valid;
            if (st6_valid) begin
                st7_val <= (st6_val >= M_TOTAL_X2) ? sub2 : st6_val;
            end
        end
    end

    // --------------------------------------------------------------------------
    // PIPELINE STAGE 8: Final Modulo Reduction (Step 4: 1*M) & Output
    // --------------------------------------------------------------------------
    wire [139:0] sub1 = st7_val - M_TOTAL_X1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            out_valid <= 1'b0;
            out_X     <= 64'd0;
        end else begin
            out_valid <= st7_valid;
            if (st7_valid) begin
                out_X <= (st7_val >= M_TOTAL_X1) ? sub1[63:0] : st7_val[63:0];
            end
        end
    end

endmodule
