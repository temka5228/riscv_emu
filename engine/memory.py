# memory.py

class Memory:
    def __init__(self, size=4096):
        self.__memory = bytearray(size)

    
    def read(self, address:int | slice) -> bytearray:
        if type(address) == slice:
            if address.stop >= len(self.__memory):
                raise ValueError("Address out of range", address)
        return self.__memory[address]

    def write(self, address, value):
        '''
        if not (0 <= address < len(self.__memory)):
            raise ValueError("Address out of range")'
        '''
        self.__memory[address] = value

    def asDict(self):
        result = {}
        for i in range(0, len(self.__memory), 4):
            chunk = self.__memory[i:i+4]
            value = int.from_bytes(chunk, byteorder='little', signed=False)

            start_addr = i
            end_addr = i + 3
            addr_key = f'0x{start_addr:04x}-0x{end_addr:04x}'

            result[addr_key] = f'0x{value:08x}'
        return result
    
    def set_size(self, new_size):
        size = len(self.__memory)
        if new_size > size:
            self.__memory.extend(bytearray(new_size - size))
        elif new_size == size:
            pass
        else:
            self.__memory = self.__memory[0:new_size]

    def __getitem__(self, key):
        return self.read(key)

    def __setitem__(self, key, value):
        self.write(key, value)

    def __repr__(self):
        return f"Memory({self.__memory})"

