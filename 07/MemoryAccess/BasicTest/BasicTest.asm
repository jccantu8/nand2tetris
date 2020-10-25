@10 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

(POP_TEMP_1) //pop local
@0
D=A
@LCL
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

(POP_TEMP_2) //pop argument
@2
D=A
@ARG
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

(POP_TEMP_3) //pop argument
@1
D=A
@ARG
D=M+D
@POP_TEMP_3
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_3
A=M
M=D

@36 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

(POP_TEMP_4) //pop this
@6
D=A
@THIS
D=M+D
@POP_TEMP_4
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_4
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

(POP_TEMP_5) //pop that
@5
D=A
@THAT
D=M+D
@POP_TEMP_5
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_5
A=M
M=D

(POP_TEMP_6) //pop that
@2
D=A
@THAT
D=M+D
@POP_TEMP_6
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_6
A=M
M=D

@510 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

(POP_TEMP_6) //pop temp
@6
D=A
@5
D=A+D
@POP_TEMP_6
M=D
@SP
M=M-1
@SP
A=M
D=M
@POP_TEMP_6
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

