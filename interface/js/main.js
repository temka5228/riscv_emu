const { app, BrowserWindow, ipcMain, dialog} = require('electron/main')
const { spawn } = require('child_process')
const { json } = require('stream/consumers')
const path = require('path')
const execFile = require('child_process').execFile
const fs = require('fs')

const INDEX_PATH = path.join(__dirname, '../riscv_emu.html')

let pythonProcess = null

function startPythonBackend() {
  const venvPath = path.join(__dirname, '../../.venv')
  const pythonSciptPath = path.join(__dirname, '../../engine/main.py')
  pythonExecutable = path.join(venvPath, 'Scripts', 'python.exe')
  console.log('python path exists', fs.existsSync(pythonExecutable))
  console.log(pythonExecutable)
  const pythonProcess = spawn(pythonExecutable, [pythonSciptPath])

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`)
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error ${data}`)
  })

  pythonProcess.on('close', (code) => {
    console.log(`Python closed with code ${code}`)
  })
}


const createWindow = () => {
  const win = new BrowserWindow({
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    height: 600,
    width: 800,
    minHeight: 600,
    minWidth: 800,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#23272a',
    },
    frame: false,
    transparent: true,
    backgroundColor: '#00ffffff'
  })

  win.webContents.openDevTools()
  win.loadFile(INDEX_PATH)

  ipcMain.handle('start-emulation', (_, binaryString, startPosition) => {
    fetch('http://localhost:8000/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        file_path: binaryString,
        address: startPosition
      })
    })
  })

}

app.whenReady().then(() => {
  startPythonBackend()
  createWindow()
  process.traceProcessWarnings = true


  /*
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })*/
})

app.on('before-quit', () => {
  execFile().kill("SIGINT")
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})