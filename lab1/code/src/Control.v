module Control
(
    op_i,
    ALUOp,
    ALUSrc,
    RegWrite_i
);

input   [6:0]   op_i;
output  [1:0]   ALUOp;
output          ALUSrc;
output          RegWrite_i;

assign  ALUOp = (op_i == 7'b0110011) ? 2'b00 : 2'b01;

assign  ALUSrc = (op_i == 7'b0110011) ? 1'b0 : 1'b1;

assign  RegWrite_i = 1'b1;


endmodule