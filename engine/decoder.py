from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import riscv_emu

class Decoder:
    def __init__(self, emu: riscv_emu.RISCVEmu):
        self.emu = emu
    
    def decode(self, instruction:int):
        opcode = (instruction >> 2) & 0x1F # код операции 6-2
        #print('in decode method', instruction, hex(instruction >> 2), hex(opcode))
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
                funct3 = (instruction >> 12) & 0x07 
                rs1 = (instruction >> 15) & 0x1F
                imm = (instruction >> 20)
                match funct3:
                    case 0x00: return {'type': 'addi', 'rd': rd, 'rs1': rs1, 'imm': imm} # сложить rs1 с знаковым расширеным числом
                    case 0x02: return {'type': 'slti', 'rd': rd, 'rs1': rs1, 'imm': imm} # сравнение rs1 со знаковым расширеным числом
                    case 0x03: return {'type': 'sltui', 'rd': rd, 'rs1': rs1, 'imm': imm} # сравнение rs1 с беззнаковым расширеным числом
                    case 0x04: return {'type': 'xori', 'rd': rd, 'rs1': rs1, 'imm': imm} # xor 
                    case 0x06: return {'type': 'ori', 'rd': rd, 'rs1': rs1, 'imm': imm} # or
                    case 0x07: return {'type': 'andi', 'rd': rd, 'rs1': rs1, 'imm': imm} # and
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
                funct2625 = (instruction >> 25) & 0x03
                match funct2625:
                    case 0b00:
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
                    case 0b01:
                        match funct3:
                            case 0b111:
                                #print('decode remu')
                                return {'type': 'remu', 'rd': rd, 'rs1': rs1, 'rs2': rs2}

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
                funct3 = (instruction >> 12) & 0x07
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
                        return {'type': 'csrrwi', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b110:
                        return {'type': 'csrrsi', 'rd': rd, 'rs1': rs1, 'csr': csr}
                    case 0b111:
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
                                if (instruction >> 12) & 0x08 == 0b000 and (instruction >> 25) == 0x05:
                                    return {'type': 'sfence.vma', 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                                else: raise Exception(f'Unknown instruction: {hex(opcode)}')
                    case _:
                        raise Exception(f'Unknown funct3: {hex(funct3)}')
            case 0x00:
                rd = (instruction >> 7) & 0x1F
                funct3 = (instruction >> 12) & 0x07
                rs1 = (instruction >> 15) & 0x1F
                offset = (instruction >> 20)
                match funct3:
                    case 0b000: # Загрузить 8-битное число из памяти и знаково расширить
                        return {'type': 'lb', 'rd': rd, 'rs1': rs1, 'offset': offset}
                    case 0b001: # Загрузить 16-битное число из памяти и знакого расширить
                        return {'type': 'lh', 'rd': rd, 'rs1': rs1, 'offset': offset}
                    case 0b010: # Загрузить 32-битное число из памяти и знакого расширить
                        return {'type': 'lw', 'rd': rd, 'rs1': rs1, 'offset': offset}
                    case 0b100: # Загрузить 8-битное число из памяти и расширить нулями
                        return {'type': 'lbu', 'rd': rd, 'rs1': rs1, 'offset': offset}
                    case 0b101: # Загрузить 16-битное число из памяти и расширить нулями
                        return {'type': 'lhu', 'rd': rd, 'rs1': rs1, 'offset': offset}
                    case _: raise Exception(f'Unknown funct3 in 0x00: {hex(funct3)}')

            case 0x08:
                offset = ((instruction >> 25) << 5 ) | (instruction >> 7) & 0x1F
                rs1 = (instruction >> 15) & 0x1F
                rs2 = (instruction >> 20) & 0x1F
                funct3 = (instruction >> 12) & 0x07
                match funct3:
                    case 0b000: # Помещает 8-битное число с младших битов rs2 в память
                        return {'type': 'sb', 'rs1': rs1, 'rs2': rs2}
                    case 0b001: # Помещает 16 младших бит числа rs2 в память
                        return {'type': 'sh', 'rs1': rs1, 'rs2': rs2}
                    case 0b010: # Помещает 32 младших бит числа rs2 в память
                        return {'type': 'sw', 'rs1': rs1, 'rs2': rs2}
                    case _: 
                        raise Exception(f'Unknown funct3 in 0x08: {hex(funct3)}')
            
            case 0x1B: # Jump to address and place return address in rd.
                offset = (((instruction >> 31) << 19) | ((instruction >> 21) & 0x3FF) << 1| \
                        ((instruction >> 20) & 0x01) << 10 | ((instruction >> 12) & 0xFF) << 11)
                rd = (instruction >> 7) & 0x1F
                return {'type': 'jal', 'rd': rd, 'offset': offset}
            
            case 0x19: # Jump to address and place return address in rd
                offset = (instruction >> 20)
                rs1 = (instruction >> 15) & 0x1F
                rd = (instruction >> 7) & 0x01F
                return {'type': 'jalr', 'rd': rd, 'rs1': rs1, 'offset': offset}
            
            case 0x18:
                funct3 = (instruction >> 12) & 0x07
                offset = (((instruction >> 31) << 11) | ((instruction >> 25) & 0x3F) << 4 | \
                        ((instruction >> 8) & 0x0F) | ((instruction >> 7) & 0x01) << 10) << 1
                rs1 = (instruction >> 15) & 0x1F
                rs2 = (instruction >> 20) & 0x1F
                match funct3: 
                    case 0b000: # Take the branch if registers rs1 and rs2 are equal.
                        return {'type': 'beq', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
                    case 0b001: # Take the branch if registers rs1 and rs2 are not equal.
                        return {'type': 'bne', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
                    case 0b100: # Take the branch if registers rs1 is less than rs2, using signed comparison.
                        return {'type': 'blt', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
                    case 0b101: # Take the branch if registers rs1 is greater than or equal to rs2, using signed comparison.
                        return {'type': 'bge', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
                    case 0b110: # Take the branch if registers rs1 is less than rs2, using unsigned comparison.
                        return {'type': 'bltu', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
                    case 0b111: # Take the branch if registers rs1 is greater than or equal to rs2, using unsigned comparison.
                        return {'type': 'bgeu', 'rs1': rs1, 'rs2': rs2, 'offset': offset}
                    case _: 
                        raise Exception(f'Unknown funct3 in 0x18: {hex(funct3)}')
            case _: 
                raise Exception(f'Unknown pd: {hex(opcode)}')