# memory.py

class Memory:
    def __init__(self, size=4096):
        self.memory = [0] * size

    def read(self, address):
        if not (0 <= address < len(self.memory)):
            raise ValueError("Address out of range")
        return self.memory[address]

    def write(self, address, value):
        if not (0 <= address < len(self.memory)):
            raise ValueError("Address out of range")
        self.memory[address] = value

    def __repr__(self):
        return f"Memory({self.memory})"
