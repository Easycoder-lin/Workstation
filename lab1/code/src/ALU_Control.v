module ALU_Control
(
    ALUOp,
    instr_o,
    ALU_select
);

input   [1:0]   ALUOp;
input   [31:0]  instr_o;
output  [2:0]   ALU_select;

assign  ALU_select = (ALUOp == 2'b00 && instr_o[31:25] == 7'b0000000 && instr_o[14:12] == 3'b111) ? 3'b000: // and
                     (ALUOp == 2'b00 && instr_o[31:25] == 7'b0000000 && instr_o[14:12] == 3'b100) ? 3'b001: // xor
                     (ALUOp == 2'b00 && instr_o[31:25] == 7'b0000000 && instr_o[14:12] == 3'b001) ? 3'b010: // sll
                     (ALUOp == 2'b00 && instr_o[31:25] == 7'b0000000 && instr_o[14:12] == 3'b000) ? 3'b011: // add
                     (ALUOp == 2'b00 && instr_o[31:25] == 7'b0100000 && instr_o[14:12] == 3'b000) ? 3'b100: // sub                   
                     (ALUOp == 2'b00 && instr_o[31:25] == 7'b0000001 && instr_o[14:12] == 3'b000) ? 3'b101: // mul
                     (ALUOp == 2'b01 && instr_o[14:12] == 3'b000) ? 3'b110: // addi
                     (ALUOp == 2'b01 && instr_o[31:25] == 7'b0100000 && instr_o[14:12] == 3'b101) ? 3'b111: // srai
                     3'bx;

endmodule