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



(INIT)
	@8192		
	D=A
	@R0      // Save the screen address
	M=D
	
(KEY_CHCK)   // The main loop of the program
    
	@R0
	M=M-1
	D=M
	@INIT
	D;JLT
	
	@KBD
	D=M
	@PRESSED
	D;JGT
	@NOT_PRESSED
	D;JEQ

(PRESSED)
	@SCREEN
	D=A
    @R0
	A=D+M
    M=-1	// 1111111111111111
    @KEY_CHCK
    0;JMP

(NOT_PRESSED)
	@SCREEN
	D=A
    @R0
	A=D+M
    M=0		// 0000000000000000
    @KEY_CHCK
    0;JMP


	