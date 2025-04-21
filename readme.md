# RISC-v Emulator with electron frontend interface

## first of all need to build python backend module
to do this run this commands follow this steps:
1. create and activate virtual environments:
```
python -m venv .venv
# for cmd
.venv/Scripts/activate.bat
# for PowerShell
.venv/Scripts/Activate.ps1
```
2. install requirements:
```
python -m pip install -r requirements.txt
```

3. build the executable file:
```
pyinstaller riscv_emu.spec
```

## Build the electron app
1. install the nodejs package manager (npm)

2. install electron and its packages:
```
npm install electron --save-dev
```
