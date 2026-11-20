// Simplified Pong-style Hack assembly test program (NOT the official Nand2Tetris Pong)
// This program repeatedly toggles a screen word based on a simple loop.
// It is intended as a small assembler test using labels and variables.

(START)
@counter
M=0

(LOOP)
@counter
M=M+1

@SCREEN
D=A
@counter
D=D+M
@R1
M=D

@R1
A=M
M=-1

@LOOP
0;JMP