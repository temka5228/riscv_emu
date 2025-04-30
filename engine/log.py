from riscv_emu import RISCVEmu

data = [
    'bubble'
]

riscv = RISCVEmu()
for d in data:
    with open('./data/' + d + 'data.bin', 'rb') as f:
        riscv.load_binary(f.read(), 8192)

    with open('./data/' + d + '.bin', 'rb') as f:
        riscv.load_binary(f.read(), 0)

    riscv.run(0)
