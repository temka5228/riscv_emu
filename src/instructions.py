# instructions.py
from registers import Registers

class Instructions:
    def __init__(self, emu) -> None:
        self.emu = emu

    def li(self, rd, imm): #
        self.emu.registers.write(rd, imm)

    def addi(self, rd, rs1, imm):
        value = self.emu.registers.read(rs1) + imm
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
        value = self.emu.registers.read(rs1) + self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def sub(self, rd, rs1, rs2):
        value = self.emu.registers.read(rs1) - self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def and_(self, rd, rs1, rs2):
        value = self.emu.registers.read(rs1) & self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def or_(self, rd, rs1, rs2):
        value = self.emu.registers.read(rs1) | self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def xor(self, rd, rs1, rs2):
        value = self.emu.registers.read(rs1) ^ self.emu.registers.read(rs2)
        self.emu.registers.write(rd, value)

    def sll(self, rd, rs1, rs2):
        value = self.emu.registers.read(rs1) << (self.emu.registers.read(rs2) & 0x1F)
        self.emu.registers.write(rd, value)

    def srl(self, rd, rs1, rs2):
        value = self.emu.registers.read(rs1) >> (self.emu.registers.read(rs2) & 0x1F)
        self.emu.registers.write(rd, value)
