.globl __start

.rodata
    division_by_zero: .string "division by zero"

.text
__start:
    # Read first operand
    li a0, 5
    ecall
    mv s0, a0
    # Read operation
    li a0, 5
    ecall
    mv s1, a0
    # Read second operand
    li a0, 5
    ecall
    mv s2, a0

###################################
#  TODO: Develop your calculator  #
#                                 #
    slti a3, s1, 6
    beq a3, x0, state_six
    slti a3, s1, 5
    beq a3, x0, state_five
    slti a3, s1, 4
    beq a3, x0, state_four
    slti a3, s1, 3
    beq a3, x0, state_three
    slti a3, s1, 2
    beq a3, x0, state_two
    slti a3, s1, 1
    beq a3, x0, state_one
    slti a3, s1, 0
    beq a3, x0, state_zero
    
state_zero:
    add s3, s0, s2
    jal zero, output
state_one:
    sub s3, s0, s2
    jal zero, output
state_two:
    mul s3, s0, s2
    jal zero, output
state_three:
    beq s2, x0, division_by_zero_except
    div s3, s0, s2
    jal zero, output
state_four:
    slt a2, s0, s2
    beq a2, x0, ge
    add s3, s0, x0
    jal zero, output
ge:
    add s3, s2, x0
    jal zero, output
state_five:
    add a4, s2, x0
    addi a5, x0, 1
loop1:
    mul a5, a5, s0
    addi a4, a4, -1
    slti a6, a4, 1
    beq a6, x0, loop1
    add s3, a5, x0 
    jal zero, output    
state_six:
    add a4, s0, x0
    addi a5, x0, 1
loop2:
    mul a5, a5, a4
    addi a4, a4, -1
    slti a6, a4, 2
    beq a6, x0, loop2
    add s3, a5, x0 
    jal zero, output
###################################

output:
    # Output the result
    li a0, 1
    mv a1, s3
    ecall

exit:
    # Exit program(necessary)
    li a0, 10
    ecall

division_by_zero_except:
    li a0, 4
    la a1, division_by_zero
    ecall
    jal zero, exit
