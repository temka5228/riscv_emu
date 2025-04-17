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
        self.load_address = 0
        self.len_file = 0
    
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

    def load_binary(self, file, load_address=None):
        if load_address:
            self.load_address = load_address
        self.len_file = len(file)
        try:
            self.memory[self.load_address: self.load_address + self.len_file] = file
        except ValueError:
            self.running = False
        self.pc = self.load_address
        
    def fetch_instruction(self) -> int:
        self.pc &= 0xFFFF_FFFC
        try:
            instr_bytes = self.memory[self.pc:self.pc + 4]
        except ValueError:
            self.running = False
            self.pc = 0
            return 0x0
        instruction = int.from_bytes(instr_bytes, byteorder='little')
        print(f'instruction: {hex(instruction)}, programm counter: {self.pc}')
        self.pc += 4
        return instruction
    
    def get_state(self):
        return {'registers': repr(self.registers), 'memory': repr(self.memory), 'pc': self.pc}

    def decode_programm(self):
        pc = self.pc
        res = ''
        while pc < self.load_address + self.len_file:
            decodedInstruction = self.decoder.decode(int.from_bytes(self.memory[pc: pc + 4], byteorder='little'))
            for v in decodedInstruction.values():
                res += f'{v} '
            res += '<br/>'
            pc += 4
        return res

