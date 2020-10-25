@3030 //push constant
D=A
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
@THIS
M=D

@3040 //push constant
D=A
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

@32 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

(POP_TEMP_1) //pop this
@2
D=A
@THIS
D=M+D
@POP_TEMP_1
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_1
A=M
M=D

@46 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

(POP_TEMP_2) //pop that
@6
D=A
@THAT
D=M+D
@POP_TEMP_2
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_2
A=M
M=D

@THIS //push point
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT //push point
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

@2 //push this
D=A
@THIS
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

@6 //push that
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

