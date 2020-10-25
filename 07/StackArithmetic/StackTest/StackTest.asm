@17 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@17 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //eq
M=M-1
A=M
D=M
A=A-1
D=D-M
@EQUAL_LABEL_1
D;JEQ
@SP
A=M-1
M=0
@EQUAL_LABEL_1_END
0;JMP
(EQUAL_LABEL_1)
@SP
A=M-1
M=-1
(EQUAL_LABEL_1_END)

@17 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@16 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //eq
M=M-1
A=M
D=M
A=A-1
D=D-M
@EQUAL_LABEL_2
D;JEQ
@SP
A=M-1
M=0
@EQUAL_LABEL_2_END
0;JMP
(EQUAL_LABEL_2)
@SP
A=M-1
M=-1
(EQUAL_LABEL_2_END)

@16 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@17 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //eq
M=M-1
A=M
D=M
A=A-1
D=D-M
@EQUAL_LABEL_3
D;JEQ
@SP
A=M-1
M=0
@EQUAL_LABEL_3_END
0;JMP
(EQUAL_LABEL_3)
@SP
A=M-1
M=-1
(EQUAL_LABEL_3_END)

@892 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@891 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //lt
M=M-1
A=M
D=M
A=A-1
D=M-D
@LESS_THAN_LABEL_1
D;JLT
@SP
A=M-1
M=0
@LESS_THAN_LABEL_1_END
0;JMP
(LESS_THAN_LABEL_1)
@SP
A=M-1
M=-1
(LESS_THAN_LABEL_1_END)

@891 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@892 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //lt
M=M-1
A=M
D=M
A=A-1
D=M-D
@LESS_THAN_LABEL_2
D;JLT
@SP
A=M-1
M=0
@LESS_THAN_LABEL_2_END
0;JMP
(LESS_THAN_LABEL_2)
@SP
A=M-1
M=-1
(LESS_THAN_LABEL_2_END)

@891 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@891 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //lt
M=M-1
A=M
D=M
A=A-1
D=M-D
@LESS_THAN_LABEL_3
D;JLT
@SP
A=M-1
M=0
@LESS_THAN_LABEL_3_END
0;JMP
(LESS_THAN_LABEL_3)
@SP
A=M-1
M=-1
(LESS_THAN_LABEL_3_END)

@32767 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //gt
M=M-1
A=M
D=M
A=A-1
D=M-D
@GREATER_THAN_LABEL_1
D;JGT
@SP
A=M-1
M=0
@GREATER_THAN_LABEL_1_END
0;JMP
(GREATER_THAN_LABEL_1)
@SP
A=M-1
M=-1
(GREATER_THAN_LABEL_1_END)

@32766 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@32767 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //gt
M=M-1
A=M
D=M
A=A-1
D=M-D
@GREATER_THAN_LABEL_2
D;JGT
@SP
A=M-1
M=0
@GREATER_THAN_LABEL_2_END
0;JMP
(GREATER_THAN_LABEL_2)
@SP
A=M-1
M=-1
(GREATER_THAN_LABEL_2_END)

@32766 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@32766 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //gt
M=M-1
A=M
D=M
A=A-1
D=M-D
@GREATER_THAN_LABEL_3
D;JGT
@SP
A=M-1
M=0
@GREATER_THAN_LABEL_3_END
0;JMP
(GREATER_THAN_LABEL_3)
@SP
A=M-1
M=-1
(GREATER_THAN_LABEL_3_END)

@57 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@31 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@53 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

@112 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //sub
M=M-1
A=M
D=M
A=A-1
M=M-D

@SP //neg
A=M
A=A-1
M=-M

@SP //and
M=M-1
A=M
D=M
A=A-1
M=M&D

@82 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //or
M=M-1
A=M
D=M
A=A-1
M=D|M

@SP //not
A=M
A=A-1
M=!M

