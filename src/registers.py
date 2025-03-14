# register_file.py

class Registers:
    def __init__(self, length=32):
        self.__registers = [0] * length

    def read(self, reg_num:int) -> int:
        if not (0 <= reg_num < 32):
            raise ValueError("Register number out of range")
        return self.__registers[reg_num]

    def write(self, reg_num: int, value: int) -> None:
        if reg_num == 0:  # x0 (zero) is hardwired to zero
            return
        if not (0 <= reg_num < 32):
            raise ValueError("Register number out of range")
        self.__registers[reg_num] = value

    def __repr__(self):
        return f"RegisterFile({self.registers})"
