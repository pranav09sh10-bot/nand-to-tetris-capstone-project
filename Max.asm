// Computes max(R0, R1) and stores the result in R2

@R0
D=M
@R1
D=D-M
@OUTPUT_FIRST
D;JGT
@R1
D=M
@R2
M=D
@END
0;JMP
(OUTPUT_FIRST)
@R0
D=M
@R2
M=D
(END)
@END
0;JMP