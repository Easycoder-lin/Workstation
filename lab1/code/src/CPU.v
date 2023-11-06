module CPU
(
    clk_i, 
    rst_i,
);

// Ports
input               clk_i;
input               rst_i;

// Instructuin Memory
wire    [31:0]  instr_o;

// Control
wire    [6:0]   op_i;
wire    [1:0]   ALUOp;
wire            ALUSrc;
assign  op_i = instr_o[6:0];

// PC
wire    [31:0]  pc_i;
wire    [31:0]  pc_o;
wire    [31:0]  add_pc_o;

// Registers
// wire    [4:0]   RS1addr_i;
// wire    [4:0]   RS2addr_i;
// wire    [4:0]   RDaddr_i;
// wire    [31:0]  RDdata_i; 
wire    [31:0]  RS1data_o;
wire    [31:0]  RS2data_o;
wire            RegWrite_i;

// ALU
// wire    [31:0]   ALU_data1;
wire    [31:0]   ALU_data2;
wire    [2:0]    ALU_select;
wire    [31:0]   ALU_result;

// Sign Extend
wire    [31:0]  imm_data_o;


Control Control
(
    op_i,
    ALUOp,
    ALUSrc,
    RegWrite_i
);

Adder Add_PC
(
    pc_o,
    32'd4,
    add_pc_o
);

assign  pc_i = add_pc_o[31:0];
PC PC
(
    clk_i, 
    rst_i,
    pc_i,
    pc_o
);

Instruction_Memory Instruction_Memory
(
    pc_o,
    instr_o
);

Registers Registers
(
    rst_i,
    clk_i,
    instr_o[19:15],
    instr_o[24:20],
    instr_o[11:7], 
    ALU_result,
    RegWrite_i, 
    RS1data_o, 
    RS2data_o
);

MUX32 MUX_ALUSrc
(
    ALUSrc,
    RS2data_o,
    imm_data_o,
    ALU_data2
);

Sign_Extend Sign_Extend
(
    instr_o,
    imm_data_o
);
  
ALU ALU
(
    RS1data_o,
    ALU_data2,
    ALU_select,
    ALU_result
);

ALU_Control ALU_Control
(
    ALUOp,
    instr_o,
    ALU_select
);

endmodule

