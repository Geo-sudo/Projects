// R2 = R0 * R1

@R2
M=0

// D = R0 - R1
@R0
D=M
@R1
D=D-M

@LOOP_R0
D;JLE

@LOOP_R1
D;JGT

(LOOP_R0)
// if R0 == 0; END
    @R0
    D=M
    @END
    D;JEQ

// R2 = R2 + R0
    @R1
    D=M
    @R2
    M=D+M

// R0 = R0 - 1
    @R0
    M=M-1

// jmp LOOP
    @LOOP_R0
    0;JMP


(LOOP_R1)
// if R1 == 0; END
    @R1
    D=M
    @END
    D;JEQ

// R2 = R2 + R0
    @R0
    D=M
    @R2
    M=D+M

// R1 = R1 - 1
    @R1
    M=M-1

// jmp LOOP
    @LOOP_R1
    0;JMP

// END
(END)
    @END
    0;JMP