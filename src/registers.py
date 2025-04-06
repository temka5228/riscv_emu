# register_file.py

class Registers:
    def __init__(self, length=32):
        self.__registers = dict.fromkeys(range(length), 0)

    def read(self, reg_num:int) -> int:
        if not (0 <= reg_num < 32):
            raise ValueError("Register number out of range")
        return self.__registers[reg_num]

    def write(self, reg_num: int, value: int) -> None:
        if reg_num == 0:  # x0 (zero) is hardwired to zero
            return
        if not (0 <= reg_num < 32):
            raise ValueError("Register number out of range")
        self.__registers[reg_num] = value & 0xFFFF_FFFF

    def __repr__(self):
        return f"RegisterFile({self.registers})"
    
    def __str__(self):
        keyarr = list(map(lambda x: 'X' + str(x), self.__registers.keys()))
        reg = dict(zip(keyarr, self.__registers.values()))
        return f'Registers list:\n{reg}'
    
    def __setitem__(self, key:int, value: int):
        self.write(key, value)

    def __getitem__(self, key:int):
        return self.read(key)
