@0 //push constant
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

(LOOP_START) //label

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

@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

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

@1 //push constant
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

@0 //pop argument
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

@SP //if
M=M-1
A=M
D=M
@LOOP_START
D;JNE

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

