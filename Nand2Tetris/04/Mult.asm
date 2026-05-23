// R2 = R0 * R1

@R2
M=0

(LOOP)
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
    @LOOP
    0;JMP

// END
(END)
    @END
    0;JMP