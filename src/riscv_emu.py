# riscv_emu.py
from registers import Registers
from memory import Memory
from decoder import Decoder
from instructions import Instructions

class RISCVEmu:
    def __init__(self, memory_size:int=4096):
        self.registers = Registers()
        self.csr = Registers(1024)
        self.memory = Memory(memory_size)
        self.pc = 4  # Program Counter
        self.running = True
        self.instructions = Instructions(self)
        self.decoder = Decoder(self)
    
    def fetch(self):
        return self.memory.read(self.pc)
    
    def run(self, filename, load_address = 0x0) -> None:
        self.load_binary(filename, load_address)
        for i in range(100):
            try:
                instruction = self.fetch_instruction()
                self.decoder.execute_instruction(instruction)
            except Exception as c:
                print(c)
                break

    def load_binary(self, filename, load_address):
        with open(filename, 'rb') as f:
            binary_data = f.read()
        self.memory[load_address: load_address + len(binary_data)] = binary_data
        self.pc = load_address
        #print(self.memory[14:18])
        
    def fetch_instruction(self) -> int:
        instr_bytes = self.memory[self.pc:self.pc + 4]
        instruction = int.from_bytes(instr_bytes, byteorder='little')
        print(f'instruction: {hex(instruction)}, programm counter: {self.pc}')
        self.pc += 4
        return instruction

    


