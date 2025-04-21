# instructions.py
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import riscv_emu
#from riscv_emu import RISCVEmu

def sextToInt(number, len_significant):
    # Converts sign extended number to integer to work with
    sign = number >> len_significant
    if sign == 1:
        mask = (1 << len_significant) - 1
        signextended_number = - (((number & mask) - 1) ^ mask)
        return signextended_number
    else:
        return number
      

class Instructions:
    def __init__(self, emu: riscv_emu.RISCVEmu) -> None:
        self.emu = emu

    def lui(self, rd, imm):
        '''Build 32-bit constants and uses the U-type format. 
        LUI places the U-immediate value in the top 20 bits 
        of the destination register rd, filling in the lowest 12 bits with zeros.'''
        imm = sextToInt(imm << 12, 31)
        self.emu.registers[rd] = imm
    
    def auipc(self, rd, imm, pc):
        '''Build pc-relative addresses and uses the U-type format. 
        AUIPC forms a 32-bit offset from the 20-bit U-immediate, 
        filling in the lowest 12 bits with zeros, adds this offset to the pc, 
        then places the result in register rd.'''
        value = self.emu.memory[pc] + sextToInt(imm << 12, 31)
        self.emu.registers[rd] = value

    def addi(self, rd, rs1, imm):
        '''Adds the sign-extended 12-bit immediate to register rs1. 
        Arithmetic overflow is ignored and the result is simply the low XLEN bits
        of the result. ADDI rd, rs1, 0 is used to implement the MV rd, 
        rs1 assembler pseudo-instruction.'''
        value = self.emu.registers[rs1] + sextToInt(imm, 11)
        self.emu.registers[rd] = value

    def slti(self, rd, rs1, imm):
        # I GUESS IT WORK
        '''Place the value 1 in register rd if register rs1 is less than the signextended 
        immediate when both are treated as signed numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers[rs1] < sextToInt(imm, 11) else 0
        self.emu.registers.write(rd, value)

    def sltiu(self, rd, rs1, imm):
        #NEED TO REFACTOR!!!
        '''Place the value 1 in register rd if register rs1 is less than the immediate
        when both are treated as unsigned numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers.read(rs1) < imm else 0
        self.emu.registers.write(rd, value)

    def xori(self, rd, rs1, imm):
        '''Performs bitwise XOR on register rs1 and the sign-extended 12-bit immediate
        and place the result in rd 
        Note, “XORI rd, rs1, -1” performs a bitwise logical inversion of register 
        rs1(assembler pseudo-instruction NOT rd, rs)'''
        value = self.emu.registers.read(rs1) ^ sextToInt(imm, 11)
        self.emu.registers.write(rd, value)
    
    def ori(self, rd, rs1, imm):
        '''Performs bitwise OR on register rs1 and the sign-extended 
        12-bit immediate and place the result in rd'''
        value = self.emu.registers.read(rs1) | sextToInt(imm, 11)
        self.emu.registers.write(rd, value)

    def andi(self, rd, rs1, imm):
        '''Performs bitwise AND on register rs1 and the sign-extended 
        12-bit immediate and place the result in rd'''
        value = self.emu.registers.read(rs1) & sextToInt(imm, 11)
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
        value = self.emu.registers[rs1] >> shamt
        self.emu.registers[rd] = value
    
    def srai(self, rd, rs1, shamt):
        # hard to relize
        '''Performs arithmetic right shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of the immediate
        In RV64, bit-25 is used to shamt[5].'''
        value = self.emu.registers[rs1] >> shamt
        self.emu.registers[rd] = value

    def ecall(self):
        # Simple system call: print the value in x10
        value = self.emu.registers[10]
        print(f"Value in x10: {value}")


    def add(self, rd, rs1, rs2):
        '''Adds the registers rs1 and rs2 and stores the result in rd.
        Arithmetic overflow is ignored and the result is simply the low 
        XLEN bits of the result.'''
        value = self.emu.registers[rs1] + self.emu.registers[rs2]
        self.emu.registers[rd] = value
        #print(f'def add writed the reg {rd, self.emu.registers.read(rd)}')

    def sub(self, rd, rs1, rs2):
        '''Subs the register rs2 from rs1 and stores the result in rd.
        Arithmetic overflow is ignored and the result is simply the low 
        XLEN bits of the result.'''
        value = self.emu.registers[rs1] - self.emu.registers[rs2]
        self.emu.registers[rd] = value
    
    def slt(self, rd, rs1, rs2):
        '''Place the value 1 in register rd if register rs1 is less than register 
        rs2 when both are treated as signed numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers[rs1] < self.emu.registers[rs2] else 0
        self.emu.registers[rd] = value

    def sltu(self, rd, rs1, rs2):
        '''Place the value 1 in register rd if register rs1 is less than register 
        rs2 when both are treated as unsigned numbers, else 0 is written to rd.'''
        value = 1 if self.emu.registers[rs1] < self.emu.registers[rs2] else 0
        self.emu.registers[rd] = value

    def and_(self, rd, rs1, rs2):
        '''Performs bitwise AND on registers rs1 and rs2 and place the result in rd'''
        value = self.emu.registers[rs1] & self.emu.registers[rs2]
        self.emu.registers[rd] = value

    def or_(self, rd, rs1, rs2):
        '''Performs bitwise OR on registers rs1 and rs2 and place the result in rd'''
        value = self.emu.registers[rs1] | self.emu.registers[rs2]
        self.emu.registers[rd] = value

    def xor(self, rd, rs1, rs2):
        '''Performs bitwise XOR on registers rs1 and rs2 and place the result in rd'''
        value = self.emu.registers[rs1] ^ self.emu.registers[rs2]
        self.emu.registers[rd] = value

    def sll(self, rd, rs1, rs2):
        '''Performs logical left shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of register rs2.'''
        value = self.emu.registers[rs1] << (self.emu.registers[rs2] & 0x1F)
        self.emu.registers[rd] = value

    def srl(self, rd, rs1, rs2):
        '''Logical right shift on the value in register rs1 by the shift 
        amount held in the lower 5 bits of register rs2'''
        value = self.emu.registers[rs1] >> (self.emu.registers[rs2] & 0x1F)
        self.emu.registers[rd] = value

    def sra(self, rd, rs1, rs2):
        '''Performs arithmetic right shift on the value in register rs1 by the shift
        amount held in the lower 5 bits of register rs2'''
        value = self.emu.registers[rs1] >> (self.emu.registers[rs2] & 0x1F)
        self.emu.registers[rd] = value
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
        self.emu.registers[rd] = self.emu.csr[csr]
        self.emu.csr[csr] = self.emu.registers[rs1]

    def csrrs(self, rd, rs1, csr):
        '''Reads the value of the CSR, zero-extends the value to XLEN bits, and writes it to integer register rd.
        The initial value in integer register rs1 is treated as a bit mask that specifies bit positions to be set in the CSR.'''
        value = self.emu.csr[csr]
        self.emu.csr[csr] = value | self.emu.registers[rs1]
        self.emu.registers[rd] = value

    def csrrc(self, rd, rs1, csr):
        value = self.emu.csr[csr]
        self.emu.csr[csr] = value & ~self.emu.registers[rs1]
        self.emu.registers[rd] = value

    def csrrwi(self, rd, uimm, csr):
        '''Update the CSR using an XLEN-bit value obtained by zero-extending 
        a 5-bit unsigned immediate (uimm[4:0]) field encoded in the rs1 field.'''
        self.emu.registers[rd] = self.emu.csr.read(csr)
        self.emu.csr[csr] = uimm

    def csrrsi(self, rd, uimm, csr):
        '''Set CSR bit using an XLEN-bit value obtained by zero-extending 
        a 5-bit unsigned immediate (uimm[4:0]) field encoded in the rs1 field.'''
        self.emu.registers[rd] = self.emu.csr[csr]
        self.emu.csr[csr] = self.emu.csr.read(csr) | uimm

    def csrrci(self, rd, uimm, csr):
        '''Clear CSR bit using an XLEN-bit value obtained by zero-extending 
        a 5-bit unsigned immediate (uimm[4:0]) field encoded in the rs1 field.'''
        value = self.emu.csr[csr]
        self.emu.csr[csr] = value & ~uimm
        self.emu.registers[rd] = value
    
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
        raise Exception(f'ENDPOINT "WFI"')

    def sfencevma(self, rd, rs1, rs2):
        pass
    #sext
    def lb(self, rd, rs1, offset):
        '''Loads a 8-bit value from memory and sign-extends 
        this to XLEN bits before storing it in register rd.'''
        offset = sextToInt(offset, 11)
        value = self.emu.memory[self.emu.registers[rs1] + offset] & 0xFF
        self.emu.registers[rd] = sextToInt(value, 7)
    #sext
    def lh(self, rd, rs1, offset):
        '''Loads a 16-bit value from memory and sign-extends 
        this to XLEN bits before storing it in register rd.'''
        offset = sextToInt(offset, 11)
        value = self.emu.memory[self.emu.registers[rs1] + offset] & 0xFFFF
        self.emu.registers[rd] = sextToInt(value, 15)
    #sext
    def lw(self, rd, rs1, offset):
        '''Loads a 32-bit value from memory and sign-extends 
        this to XLEN bits before storing it in register rd.'''
        offset = sextToInt(offset, 11)
        value = self.emu.memory[self.emu.registers[rs1] + offset] & 0xFFFF_FFFF
        self.emu.registers[rd] = sextToInt(value, 31)
    
    def lbu(self, rd, rs1, offset):
        '''Loads a 8-bit value from memory and zero-extends this to XLEN bits before storing it in register rd.'''
        offset = sextToInt(offset, 11)
        value = self.emu.memory[self.emu.registers[rs1] + offset] & 0xFF
        self.emu.registers[rd] = value

    def lhu(self, rd, rs1, offset):
        '''Loads a 16-bit value from memory and zero-extends this to XLEN bits before storing it in register rd.'''
        offset = sextToInt(offset, 11)
        value = self.emu.memory[self.emu.registers[rs1] + offset] & 0xFFFF
        self.emu.registers[rd] = value

    def sb(self, offset, rs1, rs2):
        offset = sextToInt(offset, 11)
        value = self.emu.registers[rs2] & 0xFF
        self.emu.memory[self.emu.registers[rs1] + offset] = value

    def sh(self, offset, rs1, rs2):
        offset = sextToInt(offset, 11)
        value = self.emu.registers[rs2] & 0xFFFF
        self.emu.memory[self.emu.registers[rs1] + offset] = value
    
    def sw(self, offset, rs1, rs2):
        offset = sextToInt(offset, 11)
        value = self.emu.registers[rs2] & 0xFFFF_FFFF
        self.emu.memory[self.emu.registers[rs1] + offset] = value
    #sext
    def jal(self, rd, offset):
        self.emu.registers[rd] = self.emu.pc + 4
        offset = sextToInt(offset, 19)
        self.emu.pc += offset - 4

    def jalr(self, rd, rs1, offset):
        value = self.emu.pc + 4
        self.emu.pc = (self.emu.registers[rs1] + sextToInt(offset, 11)) & ~1 - 4
        self.emu.registers[rd] = value

    def beq(self, rs1, rs2, offset, pc):
        #if self.emu.registers[rs1] == self.emu.registers[rs2]:
        offset = sextToInt(offset, 12)
        target = pc + offset
        taken = (self.emu.registers[rs1] == self.emu.registers[rs2])
        if self.emu.use_bp:
            self.emu.btb[pc] = target
            last_pc, pred_taken, pred_next = self.emu.last_pred
            assert last_pc == pc, "Нарушена связь fetch - execute"

            if pred_taken != taken or (taken and pred_next != target):
                #print('Промах')
                self.emu.pc = target if taken else pc + 4
            
            self.emu.bp.update(pc, taken)
        else: 
            if taken:
                self.emu.pc = target
        #pc += offset - 4

    def bne(self, rs1, rs2, offset, pc):
        offset = sextToInt(offset, 12)
        target = pc + offset
        taken = (self.emu.registers[rs1] != self.emu.registers[rs2])
        if self.emu.use_bp:
            self.emu.btb[pc] = target
            last_pc, pred_taken, pred_next = self.emu.last_pred
            assert last_pc == pc, "Нарушена связь fetch - execute"

            if pred_taken != taken or (taken and pred_next != target):
                self.emu.pc = target if taken else pc + 4
            
            self.emu.bp.update(pc, taken)
        else: 
            if taken:
                self.emu.pc = target
    
    def blt(self, rs1, rs2, offset, pc):
        offset = sextToInt(offset, 12)
        target = pc + offset
        taken = (self.emu.registers[rs1] < self.emu.registers[rs2])
        if self.emu.use_bp:
            self.emu.btb[pc] = target
            last_pc, pred_taken, pred_next = self.emu.last_pred
            assert last_pc == pc, "Нарушена связь fetch - execute"

            if pred_taken != taken or (taken and pred_next != target):
                self.emu.pc = target if taken else pc + 4
            
            self.emu.bp.update(pc, taken)
        else: 
            if taken:
                self.emu.pc = target
    #sext offset and up
    def bge(self, rs1, rs2, offset, pc):
        offset = sextToInt(offset, 12)
        target = pc + offset
        taken = (self.emu.registers[rs1] >= self.emu.registers[rs2])
        if self.emu.use_bp:
            self.emu.btb[pc] = target
            last_pc, pred_taken, pred_next = self.emu.last_pred
            assert last_pc == pc, "Нарушена связь fetch - execute"

            if pred_taken != taken or (taken and pred_next != target):
                self.emu.pc = target if taken else pc + 4
            
            self.emu.bp.update(pc, taken)
        else: 
            if taken:
                self.emu.pc = target
    #unsigned
    def bltu(self, rs1, rs2, offset, pc):
        offset = sextToInt(offset, 12)
        target = pc + offset
        taken = (abs(self.emu.registers[rs1]) < abs(self.emu.registers[rs2]))
        if self.emu.use_bp:
            self.emu.btb[pc] = target
            last_pc, pred_taken, pred_next = self.emu.last_pred
            assert last_pc == pc, "Нарушена связь fetch - execute"

            if pred_taken != taken or (taken and pred_next != target):
                self.emu.pc = target if taken else pc + 4
            
            self.emu.bp.update(pc, taken)
        else: 
            if taken:
                self.emu.pc = target
    #unsigned
    def bgeu(self, rs1, rs2, offset, pc):
        offset = sextToInt(offset, 12)
        target = pc + offset
        taken = (abs(self.emu.registers[rs1]) >= abs(self.emu.registers[rs2]))
        if self.emu.use_bp:
            self.emu.btb[pc] = target
            last_pc, pred_taken, pred_next = self.emu.last_pred
            assert last_pc == pc, "Нарушена связь fetch - execute"

            #Если промах -> откатываемся
            if pred_taken != taken or (taken and pred_next != target):
                self.emu.pc = target if taken else pc + 4
            
            self.emu.bp.update(pc, taken)
        else: 
            if taken:
                self.emu.pc = target

    """    R32M INSTRUCTIONS    """

    def remu(self, rs1, rs2, rd):
        value = self.emu.registers[rs1] % self.emu.registers[rs2]
        self.emu.registers[rd] = value
