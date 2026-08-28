`timescale 1ps / 1ps
module tb_audit_stress;
    reg clk;
    reg rst_n;
    reg in_valid;
    reg [63:0] in_X;

    wire enc_valid;
    wire [7:0] r0, r1, r2, r3, r4, r5, r6, r7;
    wire [7:0] r8, r9, r10, r11, r12, r13, r14, r15;

    wire crt_valid;
    wire [63:0] out_X;

    wire fault_detected;
    wire [4:0] fault_channel_id;

    always #5 clk = ~clk;

    rns_encoder u_encoder (
        .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_X(in_X),
        .out_valid(enc_valid),
        .out_r0(r0),   .out_r1(r1),   .out_r2(r2),   .out_r3(r3),
        .out_r4(r4),   .out_r5(r5),   .out_r6(r6),   .out_r7(r7),
        .out_r8(r8),   .out_r9(r9),   .out_r10(r10), .out_r11(r11),
        .out_r12(r12), .out_r13(r13), .out_r14(r14), .out_r15(r15)
    );

    crt_adder_tree u_crt_tree (
        .clk(clk), .rst_n(rst_n), .in_valid(enc_valid),
        .in_r0(r0),   .in_r1(r1),   .in_r2(r2),   .in_r3(r3),
        .in_r4(r4),   .in_r5(r5),   .in_r6(r6),   .in_r7(r7),
        .in_r8(r8),   .in_r9(r9),   .in_r10(r10), .in_r11(r11),
        .in_r12(r12), .in_r13(r13), .in_r14(r14), .in_r15(r15),
        .out_valid(crt_valid),
        .out_X(out_X)
    );

    jir_fault_monitor u_fault_mon (
        .clk(clk), .rst_n(rst_n), .in_valid(crt_valid),
        .in_reconstructed_X(out_X),
        .in_redundant_r0(8'(out_X % 173)),
        .in_redundant_r1(8'(out_X % 169)),
        .fault_detected(fault_detected),
        .fault_channel_id(fault_channel_id)
    );

    reg [63:0] queue [0:31];
    integer v_idx, q_idx, passed, errors;
    reg [63:0] rand_val;

    initial begin
        clk = 0;
        rst_n = 0;
        in_valid = 0;
        in_X = 0;
        passed = 0;
        errors = 0;
        for (q_idx = 0; q_idx < 32; q_idx = q_idx + 1) queue[q_idx] = 0;

        #20 rst_n = 1; #20;

        // Feed 1000 randomized 64-bit vectors
        for (v_idx = 0; v_idx < 1000; v_idx = v_idx + 1) begin
            @(posedge clk);
            in_valid <= 1'b1;
            // Generate full 64-bit pseudorandom value
            rand_val = {$random, $random};
            in_X <= rand_val;
        end

        @(posedge clk);
        in_valid <= 1'b0;

        #300;

        if (errors == 0 && passed == 1000) begin
            $display("[AUDIT_PASS] 1000/1000 random vectors passed bit-exact with 0 errors!");
        end else begin
            $display("[AUDIT_FAIL] Passed=%0d, Errors=%0d", passed, errors);
        end
        $finish;
    end

    always @(posedge clk) begin
        if (rst_n) begin
            queue[0] <= (in_valid) ? in_X : 64'd0;
            for (q_idx = 1; q_idx < 20; q_idx = q_idx + 1) queue[q_idx] <= queue[q_idx-1];

            if (crt_valid) begin
                if (out_X === queue[11]) begin
                    passed = passed + 1;
                end else begin
                    errors = errors + 1;
                    $display("Error at time %0t: Got %h, Expected %h", $time, out_X, queue[11]);
                end
            end
        end
    end
endmodule
