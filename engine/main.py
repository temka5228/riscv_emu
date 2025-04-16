from riscv_emu import RISCVEmu
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

HOST = "localhost"
PORT = 8000
app = FastAPI()
riscv = RISCVEmu()

@app.post("/start")
def start_emulation(file_path: str, address = 0x0):
    print('start_emulation')
    riscv.load_binary(file_path, address)
    return {"status": "completed"}
    riscv.run()
    return {"status": "completed"}

@app.get("/state")
def get_state():
    print('get_state')
    response = riscv.get_state()
    return response

@app.get('/')
def root():
    return HTMLResponse("<h2>Hello METANIT.COM!</h2>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)

'''
t = './data/addsub'
app = FastAPI()
riscv = RISCVEmu()
riscv.run(t, 4)
print(riscv.registers)
'''