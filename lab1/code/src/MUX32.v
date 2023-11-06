module MUX32
(
    ALUSrc,
    RS2data_o,
    imm_data_o,
    ALU_data2
);

input           ALUSrc;
input   [31:0]  RS2data_o;
input   [31:0]  imm_data_o;
output  [31:0]  ALU_data2;

assign  ALU_data2 = (ALUSrc == 1'b0) ? RS2data_o : imm_data_o;

endmodule