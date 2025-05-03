from riscv_emu import RISCVEmu
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse,PlainTextResponse
from pydantic import BaseModel
import base64
import time

HOST = "localhost"
PORT = 8000
app = FastAPI()
riscv = RISCVEmu()

class File(BaseModel):
    file_path: str

@app.post("/load/")
async def load_file(file = Body(embed=True), address= Body(embed=True)):
    #print('in python func load file', file)
    programm = bytearray(base64.b64decode(file))
    riscv.load_binary(programm, address)
    return {"status": "completed"}

@app.post('/set-address')
def set_address(start_address= Body(embed=True)):
    riscv.set_address(start_address)
    return {"status": "completed"}

@app.post('/set-memory')
def set_memory_size(size= Body(embed=True)):
    riscv.set_memory_size(size)
    return {"status": "completed"}

@app.post('/start')
async def run(address= Body(embed=True)):
    time_start = time.time()
    riscv.run(address)
    return {"command": "run", 
            "status": "completed", 
            "time":time.time() - time_start,
            "cycles":riscv.instr_count + riscv.bp_mispredict * 2,
            "prediction":riscv.bp_total,
            "mispredict":riscv.bp_mispredict}

@app.get('/stop')
async def stop():
    riscv.running = False

@app.post('/select-predictor')
def select_predictor(name= Body(embed=True)):
    riscv.select_predictor(name)
    return {'command': 'select-predictor', 'status':'completed'}

@app.post('/use-bp')
def use_bp(use= Body(embed=True)):
    riscv.use_bp = use
    return {'command': 'use-bp', 'status':'changed'}

@app.get('/decode')
def decode():
    res = riscv.decode_programm()
    return JSONResponse(res)

@app.get("/state")
def get_state():
    print('get_state')
    response = riscv.get_state()
    return response

@app.get('/')
def root():
    return HTMLResponse("<h2>Hello METANIT.COM!</h2>")

@app.get('/memory')
def get_memory():
    return riscv.memory.asDict()

@app.get('/registers')
def get_registers():
    return JSONResponse(riscv.registers.asDict())


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