// Box.asm - K = 40
// Rectangle: 16 pixels wide, 20 rows tall
// Starting row: 40

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE

// CLEAR rectangle when no key is pressed
    @17664
    D=A
    @R13
    M=D

    @20
    D=A
    @R14
    M=D

(CLEAR_LOOP)
    @R13
    A=M
    M=0

    @32
    D=A
    @R13
    M=D+M

    @R14
    D=M
    D=D-1
    @R14
    M=D

    @CLEAR_LOOP
    D;JGT

    @LOOP
    0;JMP

// DRAW rectangle when a key is pressed
(DRAW)
    @17664
    D=A
    @R13
    M=D

    @20
    D=A
    @R14
    M=D

(DRAW_LOOP)
    @R13
    A=M
    M=-1

    @32
    D=A
    @R13
    M=D+M

    @R14
    D=M
    D=D-1
    @R14
    M=D

    @DRAW_LOOP
    D;JGT

    @LOOP
    0;JMP