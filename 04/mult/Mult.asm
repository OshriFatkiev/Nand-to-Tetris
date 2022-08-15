// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	
	@R2
	M=0
	
	@R0   // Checks if RAM[0]>0
	D=M
    @R1_NEGTIVE
	D;JGT
	
	@ZERO // if RAM[0]=0
	D;JMP
	
  (R1_NEGTIVE)
    @R1   // Checks if RAM[1]>0
	D=M
	@LOOP
	D;JGT
	
	@ZERO // if RAM[1]=0
	D;JMP
	
  (LOOP)  // Adds R0 to R2, R1 times. 	
	@R0
	D=M
	
	@R2
	M=M+D 
	
	@R1 
	M=M-1
	D=M
	
	@LOOP
	D;JGT

  (ZERO) 
	
	