`timescale 1ps/1ps
module tb;
    reg [139:0] a;
    reg [139:0] b;
    reg [139:0] c;
    initial begin
        a = 140'h120de925ab00c09fd76326e49e93bf05;
        b = 140'h120de925ab00c09fd76326e49e93bf00;
        c = a % b;
        $display("c = %h", c);
    end
endmodule
