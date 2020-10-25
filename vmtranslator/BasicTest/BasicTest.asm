@10 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@0 //pop local
D=A
@LCL
D=M+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

@21 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@22 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@2 //pop argument
D=A
@ARG
D=M+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

@1 //pop argument
D=A
@ARG
D=M+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

@36 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@6 //pop this
D=A
@THIS
D=M+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

@42 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@45 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@5 //pop that
D=A
@THAT
D=M+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

@2 //pop that
D=A
@THAT
D=M+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

@510 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@6 //pop temp
D=A
@5
D=A+D
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

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

@5 //push that
D=A
@THAT
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

@6 //push this
D=A
@THIS
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@6 //push this
D=A
@THIS
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

@SP //sub
M=M-1
A=M
D=M
A=A-1
M=M-D

@6 //push temp
D=A
@5
A=A+D
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

