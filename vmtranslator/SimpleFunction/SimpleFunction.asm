(SimpleFunction.test) //function
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1

@0 //push local
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@1 //push local
D=A
@LCL
A=M+D
D=M
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

@SP //not
A=M
A=A-1
M=!M

@0 //push argument
D=A
@ARG
A=M+D
D=M
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

@1 //push argument
D=A
@ARG
A=M+D
D=M
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

@LCL //return
D=M
@R13
M=D
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP

