

(LOOP)
    // if KBD != 0; black the screen
    @KBD
    D=M
    @BLACKEN
    D;JNE
    
    // else whiten it and check again
    @WHITEN
    0;JMP



(WHITEN)
    // Loop 8192 words starting at SCREEN
    @word
    M=0

    (LOOP_WORD_W)
        // whiten word at SCREEN + word         
        @SCREEN
        D=A
        @word
        D=D+M
        A=D
        M=0
       
        // increment word
        @word
        M=M+1

        
        // check if word == 8192 and jmp to main loop
        D=M
        @8192
        D=D-A
        @LOOP
        D;JEQ

        // jmp to loop
        @LOOP_WORD_W
        0;JMP

(BLACKEN)
    // Loop 8192 words starting at SCREEN
    @word
    M=0

    (LOOP_WORD_B)
        // blacken word at SCREEN + word         
        @SCREEN
        D=A
        @word
        D=D+M
        A=D
        M=-1
       
        // increment word
        @word
        M=M+1

        
        // check if word == 8192 and jmp to main loop
        D=M
        @8192
        D=D-A
        @LOOP
        D;JEQ

        // jmp to loop
        @LOOP_WORD_B
        0;JMP


