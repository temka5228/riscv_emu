from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import riscv_emu

class Executor:
    def __init__(self, emu: riscv_emu.RISCVEmu):
        self.emu = emu

    def execute_instruction(self, decoded) -> None:
        match decoded['type']:
            case 'lui':
                self.emu.instructions.lui(decoded['rd'], decoded['imm'])
            case 'auipc':
                self.emu.instructions.auipc(decoded['rd'], decoded['imm'], decoded['pc'])
            case 'addi':
                self.emu.instructions.addi(decoded['rd'], decoded['rs1'], decoded['imm'])
            case 'slti':
                self.emu.instructions.slti(decoded['rd'], decoded['rs1'], decoded['imm'])
            case 'sltiu':
                self.emu.instructions.sltiu(decoded['rd'], decoded['rs1'], decoded['imm'])
            case 'xori':
                self.emu.instructions.xori(decoded['rd'], decoded['rs1'], decoded['imm'])
            case 'ori':
                self.emu.instructions.ori(decoded['rd'], decoded['rs1'], decoded['imm'])
            case 'andi':
                self.emu.instructions.andi(decoded['rd'], decoded['rs1'], decoded['imm'])
            case 'slli':
                self.emu.instructions.slli(decoded['rd'], decoded['rs1'], decoded['shamt'])
            case 'srli':
                self.emu.instructions.srli(decoded['rd'], decoded['rs1'], decoded['shamt'])
            case 'srai':
                self.emu.instructions.srai(decoded['rd'], decoded['rs1'], decoded['shamt'])
            case 'lw':
                self.emu.instructions.lw(decoded['rd'], decoded['rs1'], decoded['offset'])
            case 'sw':
                self.emu.instructions.sw(decoded['offset'], decoded['rs1'], decoded['rs2'])
            case 'ecall':
                self.emu.instructions.ecall()
            case 'add':
                self.emu.instructions.add(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'sub':
                self.emu.instructions.sub(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'slt':
                self.emu.instructions.slt(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'sltu':
                self.emu.instructions.sltu(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'and_':
                self.emu.instructions.and_(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'or_':
                self.emu.instructions.or_(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'xor':
                self.emu.instructions.xor(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'sll':
                self.emu.instructions.sll(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'srl':
                self.emu.instructions.srl(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'sra':
                self.emu.instructions.sra(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'fence':
                self.emu.instructions.fence(decoded['succ'], decoded['pred'])
            case 'fencei':
                self.emu.instructions.fencei()
            case 'csrrw':
                self.emu.instructions.csrrw(decoded['rd'], decoded['rs1'], decoded['csr'])
            case 'csrrs':
                self.emu.instructions.csrrs(decoded['rd'], decoded['rs1'], decoded['csr'])
            case 'csrrc':
                self.emu.instructions.csrrc(decoded['rd'], decoded['rs1'], decoded['csr'])
            case 'csrrwi':
                self.emu.instructions.csrrwi(decoded['rd'], decoded['uimm'], decoded['csr'])
            case 'csrrsi':
                self.emu.instructions.csrrsi(decoded['rd'], decoded['uimm'], decoded['csr'])
            case 'csrrci':
                self.emu.instructions.csrrc(decoded['rd'], decoded['uimm'], decoded['csr'])
            case 'ecall':
                self.emu.instructions.ecall()
            case 'ebreak':
                self.emu.instructions.ebreak()
            case 'uret':
                self.emu.instructions.uret()
            case 'sret':
                self.emu.instructions.sret()
            case 'mret':
                self.emu.instructions.mret()
            case 'wfi':
                self.emu.instructions.wfi()
            case 'sfencevma':
                self.emu.instructions.sfencevma(decoded['rd'], decoded['rs1'], decoded['rs2'])
            case 'lb':
                self.emu.instructions.lb(decoded['rd'], decoded['rs1'], decoded['offset'])
            case 'lh':
                self.emu.instructions.lh(decoded['rd'], decoded['rs1'], decoded['offset'])
            case 'lw':
                self.emu.instructions.lw(decoded['rd'], decoded['rs1'], decoded['offset'])
            case 'lbu':
                self.emu.instructions.lbu(decoded['rd'], decoded['rs1'], decoded['offset'])
            case 'lhu':
                self.emu.instructions.lhu(decoded['rd'], decoded['rs1'], decoded['offset'])
            case 'sb':
                self.emu.instructions.sb(decoded['offset'], decoded['rs1'], decoded['rs2'])
            case 'sh':
                self.emu.instructions.sh(decoded['offset'], decoded['rs1'], decoded['rs2'])
            case 'sw':
                self.emu.instructions.sw(decoded['offset'], decoded['rs1'], decoded['rs2'])
            case 'jal':
                self.emu.instructions.jal(decoded['rd'], decoded['offset'], decoded['pc'])
            case 'jalr':
                self.emu.instructions.jalr(decoded['rd'], decoded['rs1'], decoded['offset'], decoded['pc'])
            case 'beq':
                self.emu.instructions.beq(decoded['rs1'], decoded['rs2'], decoded['offset'], decoded['pc'])
            case 'bne':
                self.emu.instructions.bne(decoded['rs1'], decoded['rs2'], decoded['offset'], decoded['pc'])
            case 'blt':
                self.emu.instructions.blt(decoded['rs1'], decoded['rs2'], decoded['offset'], decoded['pc'])
            case 'bge':
                self.emu.instructions.bge(decoded['rs1'], decoded['rs2'], decoded['offset'], decoded['pc'])
            case 'bltu':
                self.emu.instructions.bltu(decoded['rs1'], decoded['rs2'], decoded['offset'], decoded['pc'])
            case 'bgeu':
                self.emu.instructions.bgeu(decoded['rs1'], decoded['rs2'], decoded['offset'], decoded['pc'])
            case 'remu':
                #print('call remu')
                self.emu.instructions.remu(decoded['rs1'], decoded['rs2'], decoded['rd'])
            case _ as t: raise Exception(f'Unknown decoded[type] = {t}')    