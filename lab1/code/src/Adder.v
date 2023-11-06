module Adder
(
    pc_o,
    add_num,
    add_pc_o
);

input   [31:0]  pc_o;
input   [31:0]  add_num;
output  [31:0]  add_pc_o;

assign  add_pc_o = pc_o + add_num;

endmodule