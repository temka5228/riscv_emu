# instructions.py
from riscv_emu import RISCVEmu

class Instructions:
    def __init__(self, emu: RISCVEmu) -> None:
        self.emu = emu

    def lui(self, rd, imm):
        '''Build 32-bit constants and uses the U-type format. 
        LUI places the U-immediate value in the top 20 bits 
        of the destination register rd, filling in the lowest 12 bits with zeros.'''
        self.emu.registers.write(rd, imm << 12)
    
    def auipc(self, rd, imm):
        '''Build pc-relative addresses and uses the U-type format. 
        AUIPC forms a 32-bit offset from the 20-bit U-immediate, 
        filling in the lowest 12 bits with zeros, adds this offset to the pc, 
        then places the result in register rd.'''
        value = self.emu.memory.read(self.emu.pc) + imm << 12
        self.emu.register.write(rd, value)

    def addi(self, rd, rs1, imm):
        '''Adds the sign-extended 12-bit immediate to register rs1. 
        Arithmetic overflow is ignored and the result is simply the low XLEN bits
        of the result. ADDI rd, rs1, 0 is used to implement the MV rd, 
        rs1 assembler pseudo-instruction.'''
        value = self.emu.registers.read(rs1) + imm
        self.emu.registers.write(rd, value)

    def slti(self, rd, rs1, imm):
        '''Place the value 1 in register rd if register rs1 is less than the signextended 
        immediate when both are treated as signed numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers.read(rs1) < imm else 0
        self.emu.registers.write(rd, value)

    def sltiu(self, rd, rs1, imm):
        '''Place the value 1 in register rd if register rs1 is less than the immediate
        when both are treated as unsigned numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers.read(rs1) < imm else 0
        self.emu.registers.write(rd, value)

    def xori(self, rd, rs1, imm):
        '''Performs bitwise XOR on register rs1 and the sign-extended 12-bit immediate
        and place the result in rd 
        Note, “XORI rd, rs1, -1” performs a bitwise logical inversion of register 
        rs1(assembler pseudo-instruction NOT rd, rs)'''
        value = self.emu.registers.read(rs1) ^ imm
        self.emu.registers.write(rd, value)
    
    def ori(self, rd, rs1, imm):
        '''Performs bitwise OR on register rs1 and the sign-extended 
        12-bit immediate and place the result in rd'''
        value = self.emu.registers.read(rs1) | imm
        self.emu.registers.write(rd, value)

    def andi(self, rd, rs1, imm):
        '''Performs bitwise AND on register rs1 and the sign-extended 
        12-bit immediate and place the result in rd'''
        value = self.emu.registers.read(rs1) & imm
        self.emu.registers.write(rd, value)
    
    def slli(self, rd, rs1, shamt):
        '''Performs logical left shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of the immediate
        In RV64, bit-25 is used to shamt[5].'''
        value = self.emu.registers.read(rs1) << shamt
        self.emu.registers.write(rd, value)

    def srli(self, rd, rs1, shamt):
        '''Performs logical right shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of the immediate
        In RV64, bit-25 is used to shamt[5].'''
        value = self.emu.registers.read(rs1) >> shamt
        self.emu.registers.write(rd, value)
    
    def srai(self, rd, rs1, shamt):
        '''Performs arithmetic right shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of the immediate
        In RV64, bit-25 is used to shamt[5].'''
        value = self.emu.registers.read(rs1) >> shamt
        self.emu.registers.write(rd, value)

    def lw(self, rd, offset, base):
        
        address = self.emu.registers.read(base) + offset
        value = self.emu.memory.read(address)
        self.emu.registers.write(rd, value)

    def sw(self, rs2, offset, base):
        address = self.emu.registers.read(base) + offset
        value = self.emu.registers.read(rs2)
        self.emu.memory.write(address, value)

    def ecall(self):
        # Simple system call: print the value in x10
        value = self.emu.registers.read(10)
        print(f"Value in x10: {value}")

    def beq(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) == self.emu.registers.read(rs2):
            self.emu.pc += (offset << 1)

    def add(self, rd, rs1, rs2):
        '''Adds the registers rs1 and rs2 and stores the result in rd.
        Arithmetic overflow is ignored and the result is simply the low 
        XLEN bits of the result.'''
        value = self.emu.registers.read(rs1) + self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def sub(self, rd, rs1, rs2):
        '''Subs the register rs2 from rs1 and stores the result in rd.
        Arithmetic overflow is ignored and the result is simply the low 
        XLEN bits of the result.'''
        value = self.emu.registers.read(rs1) - self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)
    
    def slt(self, rd, rs1, rs2):
        '''Place the value 1 in register rd if register rs1 is less than register 
        rs2 when both are treated as signed numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers.read(rs1) < self.emu.registers.read(rs2) else 0
        self.emu.registers.write(rd, value)

    def sltu(self, rd, rs1, rs2):
        '''Place the value 1 in register rd if register rs1 is less than register 
        rs2 when both are treated as unsigned numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers.read(rs1) < self.emu.registers.read(rs2) else 0
        self.emu.registers.write(rd, value)

    def and_(self, rd, rs1, rs2):
        '''Performs bitwise AND on registers rs1 and rs2 and place the result in rd'''
        value = self.emu.registers.read(rs1) & self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def or_(self, rd, rs1, rs2):
        '''Performs bitwise OR on registers rs1 and rs2 and place the result in rd'''
        value = self.emu.registers.read(rs1) | self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def xor(self, rd, rs1, rs2):
        '''Performs bitwise XOR on registers rs1 and rs2 and place the result in rd'''
        value = self.emu.registers.read(rs1) ^ self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def sll(self, rd, rs1, rs2):
        '''Performs logical left shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of register rs2.'''
        value = self.emu.registers.read(rs1) << (self.emu.registers.read(rs2) & 0x1F)
        self.emu.registers.write(rd, value)

    def srl(self, rd, rs1, rs2):
        '''Logical right shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of register rs2'''
        value = self.emu.registers.read(rs1) >> (self.emu.registers.read(rs2) & 0x1F)
        self.emu.registers.write(rd, value)

    def sra(self, rd, rs1, rs2):
        '''Performs arithmetic right shift on the value in register rs1 by the shift
        amount held in the lower 5 bits of register rs2'''
        value = self.emu.registers.read(rs1) >> (self.emu.registers.read(rs2) & 0x1F)
        self.emu.registers.write(rd, value)

    def fence(self, succ, pred):
        '''Used to order device I/O and memory accesses as viewed by other RISC-V 
        harts and external devices or coprocessors.'''
        pass

    def fencei(self):
        '''Provides explicit synchronization between writes to instruction 
        memory and instruction fetches on the same hart.'''
        pass

    def csrrw(self, rd, rs1, csr):
        '''Atomically swaps values in the CSRs and integer registers.
        CSRRW reads the old value of the CSR, zero-extends the value to XLEN bits, 
        then writes it to integer register rd.'''
        self.emu.registers.write(rd, self.emu.csr.read(csr))
        self.emu.csr.write(csr, self.emu.registers.read(rs1))

    def csrrs(self, rd, rs1, csr):
        '''Reads the value of the CSR, zero-extends the value to XLEN bits, and writes it to integer register rd.
        The initial value in integer register rs1 is treated as a bit mask that specifies bit positions to be set in the CSR.'''
        value = self.emu.csr.read(csr)
        self.emu.csr.write(csr, value | self.emu.registers.read(rs1))
        self.emu.registers.write(rd, value)

    def csrrc(self, rd, rs1, csr):
        value = self.emu.csr.read(csr)
        self.emu.csr.write(csr, value & ~self.emu.registers.read(rs1))
        self.emu.registers.write(rd, value)

    def csrrwi(self, rd, uimm, csr):
        '''Update the CSR using an XLEN-bit value obtained by zero-extending 
        a 5-bit unsigned immediate (uimm[4:0]) field encoded in the rs1 field.'''
        self.emu.registers.write(rd, self.emu.csr.read(csr))
        self.emu.csr.write(csr, uimm)

    def csrrsi(self, rd, uimm, csr):
        '''Set CSR bit using an XLEN-bit value obtained by zero-extending 
        a 5-bit unsigned immediate (uimm[4:0]) field encoded in the rs1 field.'''
        self.emu.registers.write(rd, self.emu.csr.read(csr))
        self.emu.csr.write(csr, self.emu.csr.read(csr) | uimm)

    def csrrc(self, rd, uimm, csr):
        '''Clear CSR bit using an XLEN-bit value obtained by zero-extending 
        a 5-bit unsigned immediate (uimm[4:0]) field encoded in the rs1 field.'''
        value = self.emu.csr.read(csr)
        self.emu.csr.write(csr, value & ~uimm)
        self.emu.registers.write(rd, value)
    
    def ecall(self):
        raise Exception(f'Exception on emu')
    
    def ebreak(self):
        '''Used by debuggers to cause control to be transferred back to a debugging environment.
        It generates a breakpoint exception and performs no other operation'''
        raise Exception(f'Breakpoint')
    
    def uret(self):
        return Exception(f'u-mode User')
    
    def sret(self):
        return Exception(f's-mode User')

    def mret(self):
        return Exception(f'm-mode Machine')
    
    def wfi(self):
        pass

    def sfencevma(self, rd, rs1, rs2):
        pass
    #sext
    def lb(self, rd, rs1, offset):
        '''Loads a 8-bit value from memory and sign-extends 
        this to XLEN bits before storing it in register rd.'''
        value = self.emu.memory.read(self.emu.registers.read(rs1) + offset) & 0xFF
        self.emu.registers.write(rd, value)
    #sext
    def lh(self, rd, rs1, offset):
        '''Loads a 16-bit value from memory and sign-extends 
        this to XLEN bits before storing it in register rd.'''
        value = self.emu.memory.read(self.emu.registers.read(rs1) + offset) & 0xFFFF
        self.emu.registers.write(rd, value)
    #sext
    def lw(self, rd, rs1, offset):
        '''Loads a 32-bit value from memory and sign-extends 
        this to XLEN bits before storing it in register rd.'''
        value = self.emu.memory.read(self.emu.registers.read(rs1) + offset) & 0xFFFFFFFF
        self.emu.registers.write(rd, value)
    
    def lbu(self, rd, rs1, offset):
        '''Loads a 8-bit value from memory and zero-extends this to XLEN bits before storing it in register rd.'''
        value = self.emu.memory.read(self.emu.registers.read(rs1) + offset) & 0xFF
        self.emu.registers.write(rd, value)

    def lhu(self, rd, rs1, offset):
        '''Loads a 16-bit value from memory and zero-extends this to XLEN bits before storing it in register rd.'''
        value = self.emu.memory.read(self.emu.registers.read(rs1) + offset) & 0xFFFF
        self.emu.registers.write(rd, value)

    def sb(self, offset, rs1, rs2):
        value = self.emu.registers.read(rs2) & 0xFF
        self.emu.memory.write(self.emu.registers.read(rs1) + offset, value)

    def sh(self, offset, rs1, rs2):
        value = self.emu.registers.read(rs2) & 0xFFFF
        self.emu.memory.write(self.emu.registers.read(rs1) + offset, value)
    
    def sw(self, offset, rs1, rs2):
        value = self.emu.registers.read(rs2) & 0xFFFFFFFF
        self.emu.memory.write(self.emu.registers.read(rs1) + offset, value)
    #sext
    def jal(self, rd, offset):
        self.emu.registers.write(rd, self.emu.pc + 4)
        self.emu.pc += offset

    def jalr(self, rd, rs1, offset):
        value = self.emu.pc + 4
        self.emu.pc = (self.emu.registers.read(rs1) + offset) & ~1
        self.emu.registers.write(rd, value)

    def beq(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) == self.emu.registers.read(rs2):
            self.emu.pc += offset

    def bne(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) != self.emu.registers.read(rs2):
            self.emu.pc += offset
    
    def blt(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) < self.emu.registers.read(rs2):
            self.emu.pc += offset
    #sext offset and up
    def bge(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) >= self.emu.registers.read(rs2):
            self.emu.pc += offset
    #unsigned
    def bltu(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) < self.emu.registers.read(rs2):
            self.emu.pc += offset
    #unsigned
    def bgeu(self, rs1, rs2, offset):
        if self.emu.registers.read(rs1) >= self.emu.registers.read(rs2):
            self.emu.pc += offset
    