module ALU
(
    ALU_data1,
    ALU_data2,
    ALU_select,
    RDdata_i
);

input   [31:0]  ALU_data1;
input   [31:0]  ALU_data2;
input   [2:0]   ALU_select;
output  [31:0]  RDdata_i;

assign  RDdata_i =  (ALU_select == 3'b000) ? ALU_data1 & ALU_data2 : // and 
                    (ALU_select == 3'b001) ? ALU_data1 ^ ALU_data2 : // xor
                    (ALU_select == 3'b010) ? ALU_data1 << ALU_data2 : // sll
                    (ALU_select == 3'b011) ? ALU_data1 + ALU_data2 : // add
                    (ALU_select == 3'b100) ? ALU_data1 - ALU_data2 : // sub
                    (ALU_select == 3'b101) ? ALU_data1 * ALU_data2 : // mul
                    (ALU_select == 3'b110) ? ALU_data1 + ALU_data2 : // addi
                    (ALU_select == 3'b111) ? ALU_data1 >>> ALU_data2[4:0] : // srai
                    32'b0; 

endmodule