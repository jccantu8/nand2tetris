@111 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@333 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@888 //push constant
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP //pop static
M=M-1
@SP
A=M
D=M
(StaticTest.vm.8)
@StaticTest.vm.8
M=D

@SP //pop static
M=M-1
@SP
A=M
D=M
(StaticTest.vm.3)
@StaticTest.vm.3
M=D

@SP //pop static
M=M-1
@SP
A=M
D=M
(StaticTest.vm.1)
@StaticTest.vm.1
M=D

@StaticTest.vm.3 //push static
D=M
@SP
A=M
M=D
@SP
M=M+1

@StaticTest.vm.1 //push static
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

@StaticTest.vm.8 //push static
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

