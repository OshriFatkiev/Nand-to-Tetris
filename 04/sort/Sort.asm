
	@i        		  // outer index
	M=0

(OUT)
	@R15
	D=M
	@j        		  // inner index
	M=D-1

(IN)  	  		
	@R14      
	D=M
	@j
	A=D+M             
	D=A-1          
	
	@address_1   	  // address of arr[j]
	M=D
	D=D+1             
	@address_2  	  // address of arr[j - 1]
	M=D

	@address_1
	A=M
	D=M               
	@address_2
	A=M
	D=D-M             
	@SWAP
	D;JGT             

	@j                 
	M=M-1             
	D=M
	@i
	D=D-M
	@IN           	  // if j > i jump to internal loop
	D;JGT
	@j               
	M=M+1	
	D=M
	@R15                
	D=M-D
	@OUT              // if (R14 - j) > 0 jump to external loop
	D;JGT

	@END
	0;JMP



(SWAP)          	  // Swaping arr[j-1] with arr[j]
	@address_1
	A=M
	D=M
	@value_1      	  
	M=D
	@address_2
	A=M
	D=M
	@value_2          
	M=D

	@value_2        
	D=M
	@address_1
	A=M
	M=D
	@value_1         
	D=M
	@address_2
	A=M
	M=D
 
	@j                 
	M=M-1          
	D=M
	@i
	D=D-M
	@IN               // if(j - i) > 0 jump to internal loop
	D;JGT
	@i               
	M=M+1	   			
	D=M
	@R15                
	D=M-D
	@OUT              // if(length - i ) > 0 jump to external loop 
	D;JGT

(END)
