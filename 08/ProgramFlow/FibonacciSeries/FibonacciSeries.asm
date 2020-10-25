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

@SP //pop pointer
M=M-1
@SP
A=M
D=M
@THAT
M=D

@0 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@0 //pop that
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

@1 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@1 //pop that
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

@2 //push constant
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

(MAIN_LOOP_START) //label

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
@COMPUTE_ELEMENT
D;JNE

@END_PROGRAM //goto
0;JMP

(COMPUTE_ELEMENT) //label

@0 //push that
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@1 //push that
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

@THAT //push point
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

@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

@SP //pop pointer
M=M-1
@SP
A=M
D=M
@THAT
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

@MAIN_LOOP_START //goto
0;JMP

(END_PROGRAM) //label

