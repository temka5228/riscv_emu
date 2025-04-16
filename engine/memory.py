# memory.py

class Memory:
    def __init__(self, size=4096):
        self.__memory = bytearray(size)

    
    def read(self, address:int | slice) -> bytearray:
        '''
        if not (0 <= address < len(self.__memory)):
            raise ValueError("Address out of range")
        '''
        return self.__memory[address]

    def write(self, address, value):
        '''
        if not (0 <= address < len(self.__memory)):
            raise ValueError("Address out of range")'
        '''
        self.__memory[address] = value

    def __getitem__(self, key):
        return self.read(key)

    def __setitem__(self, key, value):
        self.write(key, value)

    def __repr__(self):
        return f"Memory({self.__memory})"

