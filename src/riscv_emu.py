# riscv_emu.py

from registers import Registers
from memory import Memory
from instructions import Instructions
from decoder import Decoder

class RISCVEmu:
    def __init__(self, memory_size=4096):
        self.registers = Registers()
        self.csr = Registers(1024)
        self.memory = Memory(memory_size)
        self.pc = 0  # Program Counter
        self.running = True
        self.instructions = Instructions(self)
        self.decoder = Decoder()

    def fetch(self):
        return self.memory.read(self.pc)
    
    def run(self, instructions):
        for i in instructions:
            self.execute(i)
            

    


