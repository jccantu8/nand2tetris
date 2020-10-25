@256 //init
D=A
@SP
M=D
@Sys.vm$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.vm$ret.0)
(Sys.init) //function

@4000 //push constant
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

@5000 //push constant
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

@Sys.vm$ret.1 //call
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.vm$ret.1)

@1 //pop temp
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

(LOOP) //label

@LOOP //goto
0;JMP

(Sys.main) //function
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
@SP
A=M
M=0
@SP
M=M+1

@4001 //push constant
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

@5001 //push constant
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

@200 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@1 //pop local
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

@40 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@2 //pop local
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

@6 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@3 //pop local
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

@123 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@Sys.vm$ret.2 //call
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.vm$ret.2)

@0 //pop temp
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

@2 //push local
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@3 //push local
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@4 //push local
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

@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

@SP //add
M=M-1
A=M
D=M
A=A-1
M=D+M

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

(Sys.add12) //function

@4002 //push constant
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

@5002 //push constant
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

@12 //push constant
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

