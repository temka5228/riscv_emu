from riscv_emu import RISCVEmu




if __name__ == "__main__":
    t = './data/euclid1.bin'
    riscv = RISCVEmu()
    riscv.run(t, 4)
    print(riscv.registers)
    