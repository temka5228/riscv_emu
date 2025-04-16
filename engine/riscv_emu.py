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
        self.running = False
    
    def fetch(self):
        return self.memory.read(self.pc)
    
    def run(self) -> None:
        #self.load_binary(filename, load_address)
        self.running = True
        while self.running:
            try:
                instruction = self.fetch_instruction()
                self.decoder.execute_instruction(instruction)
            except Exception as c:
                print(c)
                self.running = False

    def load_binary(self, filename, load_address = 0x0):
        print(type(filename))
        with open(filename, 'rb') as f:
            binary_data = f.read()
        self.memory[load_address: load_address + len(binary_data)] = binary_data
        self.pc = load_address
        #print(self.memory[14:18])
        
    def fetch_instruction(self) -> int:
        self.pc &= 0xFFFF_FFFC
        instr_bytes = self.memory[self.pc:self.pc + 4]
        instruction = int.from_bytes(instr_bytes, byteorder='little')
        print(f'instruction: {hex(instruction)}, programm counter: {self.pc}')
        self.pc += 4
        return instruction
    
    def get_state(self):
        return {'registers': repr(self.registers), 'memory': repr(self.memory), 'pc': self.pc}

    


