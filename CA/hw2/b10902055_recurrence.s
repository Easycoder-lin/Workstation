.globl __start

.text

__start:
  li a0, 5 # ecall code
  ecall
  mv x10, a0
  add s3, x0, x10
  addi s2, x0, 3
  bge s3, s2, BGE3
  jal zero, output

BGE3:
  jal x1, Recur
  jal zero, output
  
output:
  li a0, 1
  mv a1, s3
  ecall
  
exit:
  li a0, 10
  ecall
  
      
Recur:
  addi sp, sp, -16
  sw x1, 8(sp)
  sw s3, 0(sp)
  addi x5, s3, -1 # x5 = n-1 
  addi s0, x0, 2
  bge x5, s0, L1
  addi sp, sp, 16
  jalr x0, 0(x1) 
L1:
  addi s3, s3, -1
  jal x1, Recur
  lw s5, 0(sp)
  sw s3, 0(sp)
  add s3, x0, s5 
  addi s3, s3, -2
  jal x1, Recur
  addi s6, s3, 0 
  lw s3, 0(sp)
  lw x1, 8(sp)
  addi sp, sp, 16
  add x8, s3, s3
  add s3, x8, s6
  jalr x0, 0(x1)
  