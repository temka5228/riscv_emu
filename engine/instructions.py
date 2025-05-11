# instructions.py
from __future__ import annotations
from typing import TYPE_CHECKING
import predictor as pr
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
        imm = sextToInt(imm << 12, 31)
        self.emu.registers[rd] = imm
    
    def auipc(self, rd, imm, pc):
        value = pc + sextToInt(imm << 12, 31)
        self.emu.registers[rd] = value

    def addi(self, rd, rs1, imm):
        value = self.emu.registers[rs1] + sextToInt(imm, 11)
        self.emu.registers[rd] = value

    def slti(self, rd, rs1, imm):
        # I GUESS IT WORK
        value = 1 if self.emu.registers[rs1] < sextToInt(imm, 11) else 0
        self.emu.registers.write(rd, value)

    def sltiu(self, rd, rs1, imm):
        #NEED TO REFACTOR!!!
        value = 1 if self.emu.registers.read(rs1) < imm else 0
        self.emu.registers.write(rd, value)

    def xori(self, rd, rs1, imm):
        value = self.emu.registers.read(rs1) ^ sextToInt(imm, 11)
        self.emu.registers.write(rd, value)
    
    def ori(self, rd, rs1, imm):
        value = self.emu.registers.read(rs1) | sextToInt(imm, 11)
        self.emu.registers.write(rd, value)

    def andi(self, rd, rs1, imm):
        value = self.emu.registers.read(rs1) & sextToInt(imm, 11)
        self.emu.registers.write(rd, value)
    
    def slli(self, rd, rs1, shamt):
        value = self.emu.registers.read(rs1) << shamt
        self.emu.registers.write(rd, value)

    def srli(self, rd, rs1, shamt):
        value = self.emu.registers[rs1] >> shamt
        self.emu.registers[rd] = value
    
    def srai(self, rd, rs1, shamt):
        # hard to relize
        value = self.emu.registers[rs1] >> shamt
        self.emu.registers[rd] = value

    def ecall(self):
        # Simple system call: print the value in x10
        match self.emu.registers[17]:
            case 1:
                print(self.emu.registers[10])
            case 4:
                print(self.emu.read_memory_word(self.emu.registers[10]))
            case 5:
                print('Enter integer number: ', end='')
                self.emu.registers[10] = input()
            case 10:
                raise Exception("Endpoint ECALL")
            case _:
                raise Exception("Error in ecall: Unknown number in R[a7]")


    def add(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] + self.emu.registers[rs2]
        self.emu.registers[rd] = value
        #print(f'def add writed the reg {rd, self.emu.registers.read(rd)}')

    def sub(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] - self.emu.registers[rs2]
        self.emu.registers[rd] = value
    
    def slt(self, rd, rs1, rs2):
        value = 1 if self.emu.registers[rs1] < self.emu.registers[rs2] else 0
        self.emu.registers[rd] = value

    def sltu(self, rd, rs1, rs2):
        value = 1 if self.emu.registers[rs1] < self.emu.registers[rs2] else 0
        self.emu.registers[rd] = value

    def and_(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] & self.emu.registers[rs2]
        self.emu.registers[rd] = value

    def or_(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] | self.emu.registers[rs2]
        self.emu.registers[rd] = value

    def xor(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] ^ self.emu.registers[rs2]
        self.emu.registers[rd] = value

    def sll(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] << (self.emu.registers[rs2] & 0x1F)
        self.emu.registers[rd] = value

    def srl(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] >> (self.emu.registers[rs2] & 0x1F)
        self.emu.registers[rd] = value

    def sra(self, rd, rs1, rs2):
        value = self.emu.registers[rs1] >> (self.emu.registers[rs2] & 0x1F)
        self.emu.registers[rd] = value
    def fence(self, succ, pred):
        pass

    def fencei(self):
        pass

    def csrrw(self, rd, rs1, csr):
        self.emu.registers[rd] = self.emu.csr[csr]
        self.emu.csr[csr] = self.emu.registers[rs1]

    def csrrs(self, rd, rs1, csr):
        value = self.emu.csr[csr]
        self.emu.csr[csr] = value | self.emu.registers[rs1]
        self.emu.registers[rd] = value

    def csrrc(self, rd, rs1, csr):
        value = self.emu.csr[csr]
        self.emu.csr[csr] = value & ~self.emu.registers[rs1]
        self.emu.registers[rd] = value

    def csrrwi(self, rd, uimm, csr):
        self.emu.registers[rd] = self.emu.csr.read(csr)
        self.emu.csr[csr] = uimm

    def csrrsi(self, rd, uimm, csr):
        self.emu.registers[rd] = self.emu.csr[csr]
        self.emu.csr[csr] = self.emu.csr.read(csr) | uimm

    def csrrci(self, rd, uimm, csr):
        value = self.emu.csr[csr]
        self.emu.csr[csr] = value & ~uimm
        self.emu.registers[rd] = value
    
    def ebreak(self):
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
        offset = sextToInt(offset, 11)
        target = self.emu.registers[rs1] + offset
        value = int.from_bytes(self.emu.memory[target: target + 1], byteorder='little')
        self.emu.registers[rd] = sextToInt(value, 7)
    #sext
    def lh(self, rd, rs1, offset):
        offset = sextToInt(offset, 11)
        target = self.emu.registers[rs1] + offset
        value = int.from_bytes(self.emu.memory[target: target + 2], byteorder='little')
        self.emu.registers[rd] = sextToInt(value, 15)
    #sext
    def lw(self, rd, rs1, offset):
        offset = sextToInt(offset, 11)
        target = self.emu.registers[rs1] + offset
        value = int.from_bytes(self.emu.memory[target: target + 4], byteorder='little')
        self.emu.registers[rd] = sextToInt(value, 31)
    
    def lbu(self, rd, rs1, offset):
        offset = sextToInt(offset, 11)
        target = self.emu.registers[rs1] + offset
        value = int.from_bytes(self.emu.memory[target: target + 1], byteorder='little')
        self.emu.registers[rd] = value

    def lhu(self, rd, rs1, offset):
        offset = sextToInt(offset, 11)
        target = self.emu.registers[rs1] + offset
        value = int.from_bytes(self.emu.memory[target: target + 2], byteorder='little')
        self.emu.registers[rd] = value

    def sb(self, offset, rs1, rs2):
        offset = sextToInt(offset, 11)
        value = self.emu.registers[rs2] & 0xFF
        target = self.emu.registers[rs1] + offset
        self.emu.memory[target:target + 1] = value.to_bytes(1, 'little')

    def sh(self, offset, rs1, rs2):
        offset = sextToInt(offset, 11)
        value = self.emu.registers[rs2] & 0xFFFF
        target = self.emu.registers[rs1] + offset
        self.emu.memory[target:target + 2] = value.to_bytes(2, 'little')
    
    def sw(self, offset, rs1, rs2):
        offset = sextToInt(offset, 11)
        value = self.emu.registers[rs2] & 0xFFFF_FFFF
        target = self.emu.registers[rs1] + offset
        self.emu.memory[target:target + 4] = value.to_bytes(4, 'little')
    #sext
    def jal(self, rd, offset, pc):
        self.emu.flush = True
        self.emu.registers[rd] = pc + 4
        offset = sextToInt(offset, 19)
        self.emu.pc = pc + offset

    def jalr(self, rd, rs1, offset, pc):
        self.emu.flush = True
        value = pc + 4
        self.emu.pc = (self.emu.registers[rs1] + sextToInt(offset, 11)) & ~1
        self.emu.registers[rd] = value

    def beq(self, rs1, rs2, offset, pc, pred_taken, pred_next_pc):
        offset = sextToInt(offset, 12)
        taken = (self.emu.registers[rs1] == self.emu.registers[rs2])
        target = pc + offset if taken else pc + 4

        self.update_ml_bp(pc, taken)
        self.use_predict(taken, pred_taken, pred_next_pc, target, pc)


    def bne(self, rs1, rs2, offset, pc, pred_taken, pred_next_pc):
        offset = sextToInt(offset, 12)
        taken = (self.emu.registers[rs1] != self.emu.registers[rs2])
        target = pc + offset if taken else pc + 4

        self.update_ml_bp(pc, taken)
        self.use_predict(taken, pred_taken, pred_next_pc, target, pc)
    
    def blt(self, rs1, rs2, offset, pc, pred_taken, pred_next_pc):
        offset = sextToInt(offset, 12)
        taken = (self.emu.registers[rs1] < self.emu.registers[rs2])
        target = pc + offset if taken else pc + 4

        self.update_ml_bp(pc, taken)
        self.use_predict(taken, pred_taken, pred_next_pc, target, pc)

    #sext offset and up
    def bge(self, rs1, rs2, offset, pc, pred_taken, pred_next_pc):
        offset = sextToInt(offset, 12)
        taken = (self.emu.registers[rs1] >= self.emu.registers[rs2])
        target = pc + offset if taken else pc + 4

        self.update_ml_bp(pc, taken)
        self.use_predict(taken, pred_taken, pred_next_pc, target, pc)

    #unsigned
    def bltu(self, rs1, rs2, offset, pc, pred_taken, pred_next_pc):
        offset = sextToInt(offset, 12)
        taken = (abs(self.emu.registers[rs1]) < abs(self.emu.registers[rs2]))
        target = pc + offset if taken else pc + 4

        self.update_ml_bp(pc, taken)
        self.use_predict(taken, pred_taken, pred_next_pc, target, pc)

    #unsigned
    def bgeu(self, rs1, rs2, offset, pc, pred_taken, pred_next_pc):
        offset = sextToInt(offset, 12)
        taken = (abs(self.emu.registers[rs1]) >= abs(self.emu.registers[rs2]))
        target = pc + offset if taken else pc + 4

        self.update_ml_bp(pc, taken)
        self.use_predict(taken, pred_taken, pred_next_pc, target, pc)

    """    RV32M INSTRUCTIONS    """

    def mul(self, rs1, rs2, rd):
        self.emu.registers[rd] = self.emu.registers[rs1] * self.emu.registers[rs2] & 0xFFFF_FFFF

    def mulh(self, rs1, rs2, rd):
        self.emu.registers[rd] = (self.emu.registers[rs1] * self.emu.registers[rs2]) >> 32

    def mulhsu(self, rs1, rs2, rd):
        self.emu.registers[rd] = (self.emu.registers[rs1] * abs(self.emu.registers[rs2])) >> 32
    
    def mulhu(self, rs1, rs2, rd):
        self.emu.registers[rd] = (abs(self.emu.registers[rs1] * self.emu.registers[rs2])) >> 32

    def div(self, rs1, rs2, rd):
        self.emu.registers[rd] = int(self.emu.registers[rs1] / self.emu.registers[rs2])

    def divu(self, rs1, rs2, rd):
        self.emu.registers[rd] = abs(int(self.emu.registers[rs1] / self.emu.registers[rs2]))

    def rem(self, rs1, rs2, rd):
        value = abs(self.emu.registers[rs1] % self.emu.registers[rs2])
        self.emu.registers[rd] = value

    def remu(self, rs1, rs2, rd):
        value = self.emu.registers[rs1] % self.emu.registers[rs2]
        self.emu.registers[rd] = value


    """    BRANCH PREDICTORS METHODS    """

    def update_ml_bp(self, pc, taken):
        if type(self.emu.bp) == pr.MLPredictor and self.emu.use_bp:
            self.emu.pred_taken_pattern = self.emu.pred_taken_pattern[1:] + str(int(taken))
            self.emu.pred_taken_json[pc] = self.emu.pred_taken_json[pc][1:] + str(int(taken))

    def use_predict(self, taken, pred_taken, pred_next_pc, target, pc):
        if self.emu.use_bp:
            self.emu.bp_total += 1
            if taken != pred_taken or (taken and pred_next_pc != target):
                self.emu.bp_mispredict += 1
                self.emu.flush = True
                self.emu.pc = target
            if taken:
                self.emu.btb[pc] = target
                self.emu.count_true += 1
            else: self.emu.count_false += 1

            if type(self.emu.bp) == pr.MLPredictor:
                self.emu.bp.update({'pc': pc, 
                                    'pred_all': self.emu.pred_taken_pattern,
                                    'pred_json': self.emu.get_log_json(pc)},
                                    taken, pred_taken)
            else:
                self.emu.bp.update(pc, taken)
        else:
            if taken:
                self.emu.flush = True
            self.emu.pc = target