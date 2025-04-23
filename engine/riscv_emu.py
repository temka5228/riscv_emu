# riscv_emu.py
from registers import Registers
from memory import Memory
from decoder import Decoder
from instructions import Instructions
from predictor import GSharePredictor, BimodalPredictor, TruePredictor
from executor import Executor

class RISCVEmu:
    def __init__(self, memory_size:int=16_384):
        self.load_address = 0
        self.len_file = 0
        self.cycle = 0
        self.pc = 0
        self.bp_total = 0
        self.bp_mispredict = 0
        self.instr_count = 0

        self.registers = Registers()
        self.csr = Registers(1024)
        self.memory = Memory(memory_size)
        self.instructions = Instructions(self)
        self.decoder = Decoder(self)
        self.executor = Executor(self)
        self.bp = GSharePredictor(history_bits=12, bht_bits=12)

        self.stall = False
        self.flush = False
        self.use_bp = False
        self.running = False

        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None

        self.btb = {}
        self.last_pred = None

    def step(self):
        self.instr_count += 1

        if self.MEM_WB:
            self.MEM_WB = None
        
        if self.EX_MEM:
            self.MEM_WB = self.EX_MEM
            self.EX_MEM = None

        if self.ID_EX and not self.stall:
            self.executor.execute_instruction(self.ID_EX)
            #print(self.registers)
            self.EX_MEM = self.ID_EX
            #print(self.EX_MEM, 'executer')
            self.ID_EX = None
        
        if self.IF_ID and not self.stall:
            instr = self.IF_ID
            decoded = self.decoder.decode(instr['raw'])
            #print(decoded, 'decoded')
            decoded['pc'] = instr['pc']
            if self.use_bp:
                decoded['pred_taken'] = instr['pred_taken']
                decoded['pred_next_pc'] = instr['pred_next_pc']

            if self.EX_MEM and 'rd' in decoded and 'rd' in self.EX_MEM:
                if decoded.get('rs1') == self.EX_MEM.get('rd') or decoded.get('rs2') == self.EX_MEM.get('rd'):
                    self.stall = True
                    #return
            else:
                self.stall = False
    
            self.ID_EX = decoded
            self.IF_ID = None

        if self.flush:
            self.ID_EX = None
            self.IF_ID = None
            self.flush = False
        elif not self.stall:
            instr_bytes = self.read_memory_word(self.pc)
            self.IF_ID = {
                'pc': self.pc,
                'raw': instr_bytes
            }
            if self.use_bp:
                pred_taken = self.bp.predict(self.pc)
                self.IF_ID['pred_taken'] = pred_taken
                self.IF_ID['pred_next_pc'] = self.btb.get(self.pc, self.pc + 4) if pred_taken else self.pc + 4
                self.pc = self.IF_ID['pred_next_pc']
            else:
                self.pc += 4
            #print(self.IF_ID, 'fetch')
        else: self.stall = False

    def run(self, address=None):
        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None
        self.instr_count = 0

        if address != None:
            self.pc = address

        self.running = True
        while self.running:

            try:
                self.step()
            except Exception as ex:
                print(f'Exception : {ex}')
                self.running = False


    def read_memory_word(self, addr):
        b = self.memory[addr:addr + 4]
        return int.from_bytes(b, byteorder='little')

    def load_binary(self, file, address):
        self.len_file = len(file)
        try:
            self.memory[address: address + self.len_file] = file
        except ValueError:
            self.running = False
        self.pc = self.load_address
    
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
        

