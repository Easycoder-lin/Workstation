module Sign_Extend
(
    instr_o,
    imm_data_i
);

input   [31:0]  instr_o;
output  [31:0]  imm_data_i;

assign  imm_data_i = {{20{instr_o[31]}}, instr_o[31:20]};

endmodule