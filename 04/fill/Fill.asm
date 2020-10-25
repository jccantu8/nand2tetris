// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@SCREEN
D=A
@addr
M=D 	// set addr to screen's base address

@i
M=0		// set i = 0

@addr
D=M
@temp
M=D 	// set temp = addr

(LOOP)
	@KBD
	D=M
	@CHANGE
	D;JNE	// jump to CHANGE if keyboard is not 0 (i.e. any key is pressed)


	(WHITELOOP)
	@temp
	A=M
	M=0		// set temp = 0 which turns pixel white

	@i
	M=M+1	// set i = i + 1
	@1
	D=A
	@temp
	M=D+M 	// add 32 to temp which means move to the next pixel

	@i
	D=M
	@8192 	// screen has 8192 pixels
	D=D-A
	@WHITELOOP
	D;JLT	// keep moving to each pixel until all are changed

	@i
	M=0		// reset i = 0

	@addr 
	D=M
	@temp
	M=D 	// reset temp = addr

	@LOOP
	0;JMP 	// infinite loop of listening to keyboard


(CHANGE)
	(BLACKLOOP)
		@temp
		A=M
		M=-1	// set temp = 0 which turns pixel black

		@i
		M=M+1	// set i = i + 1
		@1
		D=A
		@temp
		M=D+M 	// add 32 to temp which means move to the next pixel

		@i
		D=M
		@8192
		D=D-A
		@BLACKLOOP
		D;JLT	// keep moving to each pixel until all are changed

	@i
	M=0		// reset i = 0

	@addr
	D=M
	@temp
	M=D 	// reset temp = addr

	@LOOP
	0;JMP 	// infinite loop of listening to keyboard