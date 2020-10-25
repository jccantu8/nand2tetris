@7 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@8 //push constant
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

