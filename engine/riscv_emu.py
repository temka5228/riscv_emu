# riscv_emu.py
from registers import Registers
from memory import Memory
from decoder import Decoder
from instructions import Instructions
from predictor import BimodalPredictor, GSharePredictor, MLPredictor
from executor import Executor
import traceback

class RISCVEmu:
    def __init__(self, memory_size:int=32768):
        # Инициализация переменных
        self.load_address = 0
        self.len_file = 0
        self.cycle = 0
        self.pc = 0
        self.bp_total = 0
        self.bp_mispredict = 0
        self.count_true = 0
        self.count_false = 0
        self.instr_count = 0
        self.pred_count = 16

        # Инициализация модулей
        self.registers = Registers()
        self.memory = Memory(memory_size)
        self.instructions = Instructions(self)
        self.decoder = Decoder()
        self.executor = Executor(self)
        self.bp = MLPredictor()

        # Инициализация флагов состояния
        self.stall = False
        self.flush = False
        self.use_bp = False
        self.running = False

        #инициализация стадий конвейера
        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None

        # Инициализация переменных для предскзателей
        self.btb = {}
        self.pred_taken_pattern = '0' * (self.pred_count * 2)
        self.pred_taken_json = {}
        self.log_file = 'insertion.csv'

    def step(self):
        self.instr_count += 1

        if self.MEM_WB:
            self.MEM_WB = None
        
        if self.EX_MEM:
            self.MEM_WB = self.EX_MEM
            self.EX_MEM = None

        if self.ID_EX and not self.stall:
            self.executor.execute_instruction(self.ID_EX)
            self.EX_MEM = self.ID_EX
            self.ID_EX = None
        
        if self.IF_ID and not self.stall:
            instr = self.IF_ID
            decoded = self.decoder.decode(instr['raw'])
            decoded['pc'] = instr['pc']
            if self.use_bp:
                decoded['pred_taken'] = instr['pred_taken']
                decoded['pred_next_pc'] = instr['pred_next_pc']

            if self.EX_MEM and 'rd' in decoded and 'rd' in self.EX_MEM:
                if decoded.get('rs1') == self.EX_MEM.get('rd') or decoded.get('rs2') == self.EX_MEM.get('rd'):
                    self.stall = True
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
                if type(self.bp) == MLPredictor:
                    pred_taken = self.bp.predict({'pc': self.pc, 
                                    'pred_all': self.pred_taken_pattern,
                                    'pred_json': self.get_log_json(self.pc)})
                else:
                    pred_taken = self.bp.predict(self.pc)
                self.IF_ID['pred_taken'] = pred_taken
                self.IF_ID['pred_next_pc'] = self.btb.get(self.pc, self.pc + 4) if pred_taken else self.pc + 4
                self.pc = self.IF_ID['pred_next_pc']
            else:
                self.pc += 4
        else: self.stall = False

    def run(self, address=None):
        # Сброс конвейера
        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None

        # Сброс оценочных переменных
        self.instr_count = 0
        self.bp_total = 0
        self.bp_mispredict = 0
        self.count_true = 0
        self.count_false = 0

        if address != None:
            self.pc = address

        self.running = True
        while self.running:
            try:
                self.step()
            except Exception as e:
                print("Сообщение:", str(e))
                self.running = False
                
    def read_memory_word(self, addr):
        b = self.memory[addr:addr + 4]
        return int.from_bytes(b, byteorder='little')

    def load_binary(self, byte_string, address):
        self.btb = {}
        self.len_file = len(byte_string)
        try:
            self.memory[address: address + self.len_file] = byte_string
        except ValueError:
            self.running = False
        self.pc = self.load_address

    # Можно удалить
    def log_branch_info(self, pc, taken):
        with open("./data/" + self.log_file, "a") as f:
            f.write(f"{pc},{int(taken)},{self.pred_taken_pattern},{self.get_log_json(pc)}\n")

    # Можно удалить
    def get_log_json(self, pc):
        target_pc = self.pred_taken_json.get(pc, None)
        if not target_pc:
            self.pred_taken_json[pc] = '0' * self.pred_count
        return self.pred_taken_json[pc]

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

    def clear_memory(self):
        ms = self.memory.size
        del self.memory
        self.memory = Memory(ms)

    def select_predictor(self, name:str):
        name = name.lower()
        match name:
            case 'gshare':
                self.bp = GSharePredictor()
            case 'mlpredictor':
                self.bp = MLPredictor()
            case 'bimodal':
                self.bp = BimodalPredictor()
            case _ as c:
                raise Exception(f'{c} not in {['gshare', 'bimodal', 'mlpredictor']}')
        self.btb = {}

