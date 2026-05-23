

(LOOP)

    // if KBD != 0; black the screen
    // set color flag to -1
    @color
    M=-1
    @KBD
    D=M
    @CHANGE_COLOR
    D;JNE
    
    
    // else whiten it and check again
    // set color flag to 0
    @color
    M=0
    @CHANGE_COLOR
    0;JMP



(CHANGE_COLOR)
    // Loop 8192 words starting at SCREEN
    @word
    M=0

    (LOOP_WORD)
        @selected
        M=0
        // change color of selected word at SCREEN + word         
        @SCREEN
        D=A
        @word
        D=D+M

        @selected
        M=D

        @color
        D=M

        @selected
        A=M
        M=D
       
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
        @LOOP_WORD
        0;JMP
