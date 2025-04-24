	li t0, 0
	li t1, 10
loop: 	andi t2, t0, 1
	beq t2, zero, even
	addi t3, t3, 1
	jal continue
	
even: 	
	addi t4, t4, 1

continue:
	addi t0, t0, 1
	blt, t0, t1, loop 
	wfi