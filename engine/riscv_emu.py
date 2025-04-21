# riscv_emu.py
from registers import Registers
from memory import Memory
from decoder import Decoder
from instructions import Instructions
from predictor import GSharePredictor

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

        self.use_bp = False

        self.bp = GSharePredictor(history_bits=8, bht_bits=10)
        self.btb = {}
        self.last_pred = None
    
    def fetch(self):
        return self.memory.read(self.pc)
    
    def run(self, address=None) -> None:
        if address != None:
            self.pc = address

        self.running = True
        while self.running:
            try:
                instruction, pc = self.fetch_instruction()
                self.decoder.execute_instruction(instruction, pc)
            except Exception as c:
                print(f'exception ::: {c}')
                self.running = False

    def load_binary(self, file):
        self.len_file = len(file)
        try:
            self.memory[self.load_address: self.load_address + self.len_file] = file
        except ValueError:
            self.running = False
        self.pc = self.load_address
        
    def fetch_instruction(self) -> int:
        self.pc &= 0xFFFF_FFFC
        pc = self.pc

        try:
            instr_bytes = self.memory[self.pc:self.pc + 4]
            instruction = int.from_bytes(instr_bytes, byteorder='little')
        except ValueError:
            self.running = False
            self.pc = 0
            return 0x0
        
        if self.use_bp:
            taken = self.bp.predict(pc)
            if taken and pc in self.btb:
                next_pc = self.btb[pc]
            else:
                next_pc = pc + 4
            self.last_pred = (pc, taken, next_pc)
            self.pc = next_pc
        else:
            self.pc += 4
        
        #print(f'instruction: {hex(instruction)}, programm counter: {self.pc}')
        #self.pc += 4
        return instruction, pc
    
    def get_state(self):
        return {'registers': repr(self.registers), 'memory': repr(self.memory), 'pc': self.pc}

    def decode_programm(self):
        pc = self.pc
        json_res = {'bytes': '', 'decoded': ''}
        while pc < self.load_address + self.len_file:
            command = int.from_bytes(self.memory[pc:pc+4], byteorder='little')
            decodedInstruction = self.decoder.decode(command)
            for v in decodedInstruction.values():
                json_res['decoded'] += f'{v} '
            json_res['decoded'] += '<br/>'
            json_res['bytes'] += f'0x{command:08x}<br/>'
            pc += 4
        return json_res
    
    def set_address(self, address):
        if address >= 0:
            self.load_address = address

    def set_memory_size(self, size):
        self.memory.set_size(size)

    def clear_registers(self):
        del self.registers
        self.registers = Registers()
        

