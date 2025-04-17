const { app, BrowserWindow, ipcMain, dialog} = require('electron/main')
const { spawn } = require('child_process')
const { json } = require('stream/consumers')
const path = require('path')
const execFile = require('child_process').execFile
const fs = require('fs')
const waitPort = require('wait-port')

const INDEX_PATH = path.join(__dirname, '../riscv_emu.html')
const HOST = 'localhost'
const PORT = 8000
const URL = `http://${HOST}:${PORT}`

const startPythonBackend = () => {
  const venvPath = path.join(__dirname, '../../.venv')
  const pythonSciptPath = path.join(__dirname, '../../engine/main.py')
  pythonExecutable = path.join(venvPath, 'Scripts', 'python.exe')

  const pythonProcess = spawn(pythonExecutable, [pythonSciptPath])

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`);
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error ${data}`)
  })

  pythonProcess.on('error', (err) => {
    console.error('Failed to start python:', err);
  })

  pythonProcess.on('close', (code) => {
    console.log(`Python closed with code ${code}`)
  })
  return pythonProcess
}


async function createWindow () {
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
      color: '#202225',
      symbolColor: '#eaeaeb',
    },
    frame: false,
    transparent: true,
    backgroundColor: '#00ffffff'
  })

  // LOAD .HTML FILE AND OPEN DEV TOOLS
  await win.loadFile(INDEX_PATH)
  await win.webContents.openDevTools()
}

// CREATING HANDLERS
function createHandlers() {
  ipcMain.handle('run', async() => {
    response = await fetch(URL + '/start', {
      method: 'POST'
    })
    return await response.json()
  })

  ipcMain.handle('load-file', async (_, binaryString, startPosition) => {
    response = await fetch(URL + '/load/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        file_path: binaryString,
        address: startPosition
      })
    })
    return await response.ok
  })

  ipcMain.handle('get-memory', async () => {
    response = await fetch(URL + '/memory')
    return await response.json()
  })

  ipcMain.handle('get-registers', async () => {
    response = await fetch(URL + '/registers')
    return await response.json()
  })

  ipcMain.handle('decode', async () => {
    response = await fetch(URL + '/decode')
    return await response.text()
  })
  
}

// STARTUP AND SHUTDOWN
app.whenReady().then(async () => {
  try {
    pyProcess = startPythonBackend()
    await waitPort({host: HOST, port: PORT})
    createHandlers();
    await createWindow();
  } catch (err) {
    console.error('error startup: ', err)
    app.quit();
  }
  process.traceProcessWarnings = true
})

app.on('before-quit', () => {
  pyProcess.kill()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('uncaughtException', (err) => {
  console.error('Uncaught Error:', err)
})