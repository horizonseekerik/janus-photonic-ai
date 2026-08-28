`timescale 1ps/1ps
module diag_tb;
    reg clk;
    reg rst_n;
    reg in_valid;
    reg [63:0] in_X;

    wire enc_valid;
    wire [7:0] r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15;
    wire crt_valid;
    wire [63:0] out_X;

    always #5 clk = ~clk;

    rns_encoder u_enc (
        .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_X(in_X),
        .out_valid(enc_valid),
        .out_r0(r0), .out_r1(r1), .out_r2(r2), .out_r3(r3),
        .out_r4(r4), .out_r5(r5), .out_r6(r6), .out_r7(r7),
        .out_r8(r8), .out_r9(r9), .out_r10(r10), .out_r11(r11),
        .out_r12(r12), .out_r13(r13), .out_r14(r14), .out_r15(r15)
    );

    crt_adder_tree u_tree (
        .clk(clk), .rst_n(rst_n), .in_valid(enc_valid),
        .in_r0(r0), .in_r1(r1), .in_r2(r2), .in_r3(r3),
        .in_r4(r4), .in_r5(r5), .in_r6(r6), .in_r7(r7),
        .in_r8(r8), .in_r9(r9), .in_r10(r10), .in_r11(r11),
        .in_r12(r12), .in_r13(r13), .in_r14(r14), .in_r15(r15),
        .out_valid(crt_valid), .out_X(out_X)
    );

    initial begin
        clk = 0;
        rst_n = 0;
        in_valid = 0;
        in_X = 64'd12345;
        #20;
        rst_n = 1;
        #10;
        in_valid = 1;
        #10;
        in_valid = 0;
        #100;
        $finish;
    end

    always @(posedge clk) begin
        $display("T=%4t | rst=%b in_v=%b in_X=%d | enc_v=%b r0=%d r1=%d | st1_v=%b pp0=%h | st2_v=%b s0=%h | st3_v=%b s0=%h | crt_v=%b out_X=%h",
            $time, rst_n, in_valid, in_X,
            enc_valid, r0, r1,
            u_tree.st1_valid, u_tree.st1_pp0,
            u_tree.st2_valid, u_tree.st2_s0,
            u_tree.st3_valid, u_tree.st3_s0,
            crt_valid, out_X);
    end
endmodule
