# riscv_emu.py

from registers import Registers
from memory import Memory
from instructions import Instructions

class RISCVEmu:
    def __init__(self, memory_size=4096):
        self.registers = Registers()
        self.memory = Memory(memory_size)
        self.pc = 0  # Program Counter
        self.running = True
        self.instructions = Instructions(self)

    def fetch(self):
        return self.memory.read(self.pc)

    def decode(self, instruction):
        opcode = instruction & 0x7F >> 2 # код операции 6-2
        match opcode:
            case 0x0D: # lui
                rd = (instruction >> 7) & 0x1F 
                imm = instruction >> 12
                return {'type': 'lui', 'rd': rd, 'imm': imm}
            case 0x05: # auipc
                rd = (instruction >> 7) & 0x1F 
                imm = instruction >> 12
                return {'type': 'auipc', 'rd': rd, 'imm': imm}
            case 0x04: # with operand
                rd = (instruction >> 7) & 0x1F
                funct3 = (instruction >> 12) & 0x03 
                rs1 = (instruction >> 15) & 0x1F
                imm = (instruction >> 20)
                match funct3:
                    case 0x00: return {'type': 'addi', 'rd': rd, 'rs1': rs1} # сложить rs1 с знаковым расширеным числом
                    case 0x02: return {'type': 'slti', 'rd': rd, 'rs1': rs1} # сравнение rs1 со знаковым расширеным числом
                    case 0x03: return {'type': 'sltui', 'rd': rd, 'rs1': rs1} # сравнение rs1 с беззнаковым расширеным числом
                    case 0x04: return {'type': 'xori', 'rd': rd, 'rs1': rs1} # xor 
                    case 0x06: return {'type': 'ori', 'rd': rd, 'rs1': rs1} # or
                    case 0x07: return {'type': 'andi', 'rd': rd, 'rs1': rs1} # and
                    case 0x01: # левый логический сдвиг
                        shamt = (instruction >> 20) & 0x1F # кол-во бит сдвига
                        return {'type': 'slli', 'rd': rd, 'rs1': rs1, 'shamt': shamt}
                    case 0x05: # правый логиский сдвиг
                        if (instruction >> 27) == 0x00:
                            shamt = (instruction >> 20) & 0x1F # кол-во бит сдвига
                            return {'type': 'srli', 'rd': rd, 'rs1': rs1, 'shamt': shamt}
                        elif (instruction >> 27) == 0x08:
                            shamt = (instruction >> 20) & 0x1F # кол-во бит сдвига
                            return {'type': 'srai', 'rd': rd, 'rs1': rs1, 'shamt': shamt}
                        else: 
                            raise Exception(f"Unknown 31-27 bit in shifts operation: {hex(instruction >> 27)}")
                    case _:
                        raise Exception(f'Unknown funct3 in operand operation: {hex(funct3)}')
                
            case 0x0C: # регистр/регистр
                rd = (instruction >> 7) & 0x1F
                rs1 = (instruction >> 15) & 0x1F
                rs2 = (instruction >> 20) & 0x1F
                funct3 = (instruction >> 12) & 0x07
                match funct3:
                    case 0b000: # add and sub
                        match (instruction >> 27):
                            case 0x00: # сложить два числа из регистров
                                return {'type': 'add', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                            case 0x08: # вычесть из rs1 число rs2
                                return {'type': 'sub', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                            case _: raise Exception(f'Unknown 31-27 bits in add or sub: {hex(instruction >> 27)}')
                    case 0b001: # логический левый сдвиг rs1 на 5 младших битов в rs2
                        return {'type': 'sll', 'rd': rd, 'rs1': rs1, 'rs2':rs2}
                    case 0b010: # rs1 < rs2 (signed)
                        return {'type': 'slt', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b011: # rs1 < rs2 (unsigned)
                        return {'type': 'sltu', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b100: # rs1 xor rs2
                        return {'type': 'xor', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b101:
                        match instruction >> 27:
                            case 0b00000: # логический сдвиг rs1 на 5 младших битов в rs2
                                return {'type': 'srl', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                            case 0b01000: # арифметический правый сдвиг rs1 на 5 младших битов в rs2
                                return {'type': 'sra', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                            case _: 
                                raise Exception(f'Unknown 31-27 bits in reg/reg operation: {hex(instruction >> 27)}')
                    case 0b110: # rs1 or rs2
                        return {'type': 'or', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b111: # rs1 and rs2
                        return {'type': 'and', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case _: raise Exception(f'Unknown funct3 in reg/reg: {hex(funct3)}')

            case 0x03:
                funct3 = (instruction >> 12) & 0x07
                match funct3: # fence (pred, succ)
                    case 0b000:
                        succ = (instruction >> 20) & 0x0F
                        pred = (instruction >> 24) & 0x0F
                        return {'type': 'fence', 'succ': succ, 'pred': pred}
                    case 0b001:
                        return {'type': 'fence.i'}
                    case _: raise Exception(f'Unknown funct3 for fence type: {hex(funct3)}')
            
            case 0x1C:
                rd = (instruction >> 7) & 0x1F
                funct3 = (instruction >> 12) & 0x08
                rs1 = (instruction >> 15) & 0x1F
                csr = (instruction >> 20)
                match funct3:
                    case 0b001: # swap values in CSR and integer registers
                        return {'type': 'csrrw', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b010: # atomic read and set bits in CSR
                        return {'type': 'csrrs', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b011: #atomic read and clear bits in CSR
                        return {'type': 'csrrc', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b101: 
                        """Update the CSR using an XLEN-bit value obtained
                        by zero-extending a 5-bit unsigned immediate (uimm[4:0])
                        field encoded in the rs1 field."""
                        return {'type': 'csrrwi', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b110:
                        """Set CSR bit using an XLEN-bit value obtained 
                        by zero-extending a 5-bit unsigned immediate (uimm[4:0]) 
                        field encoded in the rs1 field."""
                        return {'type': 'csrrsi', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b111:
                        """Clear CSR bit using an XLEN-bit value obtained 
                        by zero-extending a 5-bit unsigned immediate (uimm[4:0]) 
                        field encoded in the rs1 field."""
                        return {'type': 'csrrci', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b000:
                        match (instruction >> 7) & 0x3FFFF:
                            case 0x0000: #ecall Make a request to the supporting execution environment.
                                return {'type': 'ecall'}
                            case 0x2000: # ebreak Used by debuggers to cause control to be transferred back to a debugging environment.
                                return {'type': 'ebreak'}
                            case 0x4000: # x ret
                                match instruction >> 27:
                                    case 0b00000: # uret Return from traps in U-mode, and URET copies UPIE into UIE, then sets UPIE.
                                        return {'type': 'uret'}
                                    case 0b00010: # sret Return from traps in S-mode, and SRET copies SPIE into SIE, then sets SPIE.
                                        return {'type': 'sret'}
                                    case 0b00110: # mret Return from traps in M-mode, and MRET copies MPIE into MIE, then sets MPIE.
                                        return {'type': 'mret'}
                                    case _: raise Exception(f'Unknown 31-27 bits in Xset: {hex(instruction >> 27)}')
                            case 0xA000: # wait for interrupt
                                return {'type': 'wfi'}
                            case _:
                                # sfence.vma Guarantees that any previous stores already visible 
                                # to the current RISC-V hart are ordered before all subsequent implicit 
                                # references from that hart to the memory-management data structures.
                                if (instruction >> 12) & 0x08 == 0b000 and (instruction >> 25) == 0x05:
                                    return {'type': 'sfence.vma', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                                else: raise Exception(f'Unknown instruction: {hex(opcode)}')
                    case _:
                        raise Exception(f'Unknown funct3: {hex(funct3)}')
            case 0x00:
                rd = (instruction >> 7) & 0x1F
                funct3 = (instruction >> 12) & 0x08
                rs1 = (instruction >> 15) & 0x1F
                offset = (instruction >> 20)
                match funct3:
                    case 0b000: # Загрузить 8-битное число из памяти и знаково расширить
                        return {'type': 'lb', 'rd': rd, 'rs1': rs1}
                    case 0b001: # Загрузить 16-битное число из памяти и знакого расширить
                        return {'type': 'lh', 'rd': rd, 'rs1': rs1}
                    case 0b010: # Загрузить 32-битное число из памяти и знакого расширить
                        return {'type': 'lW', 'rd': rd, 'rs1': rs1}
                    case 0b100: # Загрузить 8-битное число из памяти и расширить нулями
                        return {'type': 'lbu', 'rd': rd, 'rs1': rs1}
                    case 0b101: # Загрузить 16-битное число из памяти и расширить нулями
                        return {'type': 'lhu', 'rd': rd, 'rs1': rs1}
                    case _: raise Exception(f'Unknown funct3 in 0x00: {hex(funct3)}')

            case 0x08:
                offset = 


            case 0x0: # lui
                rd = (instruction >> 7) & 0x1F 
                imm = ((instruction >> 20) & 0xFFF) << 12 | (instruction >> 20) & 0xFFE00
                return {'type': 'li', 'rd': rd, 'imm': imm}
            case 0x63:  # Branch (B-Type)
                rs1 = (instruction >> 15) & 0x1F
                rs2 = (instruction >> 20) & 0x1F
                offset = ((instruction >> 7) & 0x1E) | ((instruction >> 24) & 0x7FE)
                if instruction & 0x80:
                    offset |= 0xFFFFF800
                return {'type': 'beq', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
            case 0x3:   # Load (I-Type)
                rd = (instruction >> 7) & 0x1F
                imm = ((instruction >> 12) & 0xFFF) << 12 | (instruction >> 20) & 0xFFE00
                rs1 = (instruction >> 15) & 0x1F
                return {'type': 'lw', 'rd': rd, 'offset': imm, 'base': rs1}
            case 0x23:  # Store (S-Type)
                imm = ((instruction >> 7) & 0xFE) | ((instruction >> 25) & 0x80)
                rs1 = (instruction >> 15) & 0x1F
                rs2 = (instruction >> 20) & 0x1F
                return {'type': 'sw', 'rs2': rs2, 'offset': imm, 'base': rs1}
            case 0x73:  # Environmental Call (I-Type)
                return {'type': 'ecall'}
            case 0x6F:  # Jump (J-Type)
                offset = ((instruction >> 21) & 0x7FF) | ((instruction >> 20) & 0x800) | \
                        ((instruction >> 12) & 0xFF000) | ((instruction >> 11) & 0x100000)
                return {'type': 'jal', 'rd': (instruction >> 7) & 0x1F, 'offset': offset}
            case 0x1B:  # Immediate Shift/Arithmetic
                rd = (instruction >> 7) & 0x1F
                rs1 = (instruction >> 15) & 0x1F
                imm = ((instruction >> 20) & 0xFFF) << 12 | (instruction >> 20) & 0xFFE00
                shamt = imm >> 12
                funct3 = (instruction >> 12) & 0x7
                if funct3 == 0b000:
                    return {'type': 'addi', 'rd': rd, 'rs1': rs1, 'imm': imm}
                elif funct3 == 0b011:
                    return {'type': 'sll', 'rd': rd, 'rs1': rs1, 'shamt': shamt}
                elif funct3 == 0b101:
                    return {'type': 'sr', 'rd': rd, 'rs1': rs1, 'shamt': shamt}
            case 0x3B:  # Arithmetic
                rd = (instruction >> 7) & 0x1F
                rs1 = (instruction >> 15) & 0x1F
                rs2 = (instruction >> 20) & 0x1F
                funct3 = (instruction >> 12) & 0x7
                match funct3:
                    case 0b000:
                        return {'type': 'add', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b001:
                        return {'type': 'sll', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b010:
                        return {'type': 'slt', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b011:
                        return {'type': 'sltu', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b100:
                        return {'type': 'xor', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b101:
                        return {'type': 'sr', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b110:
                        return {'type': 'or', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case 0b111:
                        return {'type': 'and', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    case _:
                        raise ()
        else:
            raise Exception(f"Unknown opcode: {hex(opcode)}")

    def execute(self, instruction):
        decoded = self.decode(instruction)
        match decoded['type']:
            case 'li':
                self.instructions.li(decoded['rd'], decoded['imm'])
            case 'addi':
            case 'lw':
            case 'ecall':
            case 'beq':

            case 'add':
            
        if decoded['type'] == 'li':
            self.instructions.li(decoded['rd'], decoded['imm'])
        elif decoded['type'] == 'addi':
            self.instructions.addi(decoded['rd'], decoded['rs1'], decoded['imm'])
        elif decoded['type'] == 'lw':
            self.instructions.lw(decoded['rd'], decoded['offset'], decoded['base'])
        elif decoded['type'] == 'sw':
            self.instructions.sw(decoded['rs2'], decoded['offset'], decoded['base'])
        elif decoded['type'] == 'ecall':
            self.instructions.ecall()
        elif decoded['type'] == 'beq':
            self.instructions.beq(decoded['rs1'], decoded['rs2'], decoded['offset'])
        elif decoded['type'] == 'add':
            self.instructions.add(decoded['rd'], decoded['rs1'], decoded['rs2'])
        elif decoded['type'] == 'sub':
            self.instructions.sub(decoded['rd'], decoded['rs1'], decoded['rs2'])
        elif decoded['type'] == 'and':
            self.instructions.and_(decoded['rd'], decoded['rs1'], decoded['rs2'])
        elif decoded['type'] == 'or':
            self.instructions.or_(decoded['rd'], decoded['rs1'], decoded['rs2'])
        elif decoded['type'] == 'xor':
            self.instructions.xor(decoded['rd'], decoded['rs1'], decoded['rs2'])
        elif decoded['type'] == 'sll':
            self.instructions.sll(decoded['rd'], decoded['rs1'], decoded['shamt'])
        elif decoded['type'] == 'srl':
            self.instructions.srl(decoded['rd'], decoded['rs1'], decoded['shamt'])
        else:
            raise Exception(f"Unknown instruction type: {decoded['type']}")

    def run(self, instructions):
        for i in instructions:
            self.execute(i)
