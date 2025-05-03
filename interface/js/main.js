const { app, BrowserWindow, ipcMain, dialog} = require('electron/main')
const { spawn, exec } = require('child_process')
const { json } = require('stream/consumers')
const path = require('path')
const execFile = require('child_process').execFile
const fs = require('fs')
const waitPort = require('wait-port')
const { ipcRenderer } = require('electron')
const isDev = require('electron-is-dev')

const INDEX_PATH = path.join(__dirname, '../riscv_emu.html')
const HOST = 'localhost'
const PORT = 8000
const URL = `http://${HOST}:${PORT}`

const API_PROD_PATH = path.join(process.resourcesPath, '../../dist/riscv_emu.exe')
const API_DEV_PATH = path.join(__dirname, "../../engine/main.py")

const startPythonBackend = () => {
  if (isDev) {
    try {
      require('electron-reloader')(module)
    } catch (_) {}
    const venvPath = path.join(__dirname, '../../.venv')
    pythonExecutable = path.join(venvPath, 'Scripts', 'python.exe')
    const pythonProcess = spawn(pythonExecutable, [API_DEV_PATH])
    return pythonProcess

  } else {
    const { pythonProcess } = execFile(API_PROD_PATH, {
      windowsHide: true
    })
    return pythonProcess

  }
}

function pythonConsole() {
  pyProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`);
    window.webContents.send('console-output', data.toString())
  })

  pyProcess.stderr.on('data', (data) => {
    console.error(`Python Error ${data}`)
    window.webContents.send('console-output', data.toString())
  })

  pyProcess.on('error', (err) => {
    console.error('Failed to start python:', err);
    window.webContents.send('console-output', data.toString())
  })

  pyProcess.on('close', (code) => {
    console.log(`Python closed with code ${code}`)
  })
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
  await win.loadFile(INDEX_PATH);
  await win.webContents.openDevTools();

  return win
}

// STARTUP AND SHUTDOWN
app.whenReady().then(async () => {
  try {
    pyProcess = startPythonBackend()
    await waitPort({host: HOST, port: PORT})
    createHandlers();
    window = await createWindow();
    pythonConsole();
  } catch (err) {
    console.error('error startup: ', err)
    app.quit();
  }
  process.traceProcessWarnings = true
})

app.on('before-quit', () => {
  if (isDev) {
    pyProcess.kill()
  } else {
    execFile().kill("SIGINT")
  }
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('uncaughtException', (err) => {
  console.error('Uncaught Error:', err)
})

// CREATING HANDLERS
function createHandlers() {
  ipcMain.handle('run', async(_, address_start) => {
    const response = await fetch(URL + '/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        address: address_start
      })
    })
    const json = await response.json()
    return {ok: response.ok, json:json}
  })

  ipcMain.handle('stop', async () => {
    fetch(URL + '/stop')
  })

  ipcMain.handle('load-file', async (_, binaryString, address) => {
    response = await fetch(URL + '/load/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        file: binaryString,
        address: address
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
    return await response.json()
  })
  
  ipcMain.handle('set-address', async (_, address) => {
    response = await fetch(URL + '/set-address', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        start_address: address
      })
    })
    return await response.json()
  })
  
  ipcMain.handle('set-memory', async (_, size) => {
    response = await fetch(URL + '/set-memory', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        size: size
      })
    })
    return await response.json()
  })

  ipcMain.handle('select-predictor', async(_, name) => {
    response = await fetch(URL + '/select-predictor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify ({
        name: name
      })
    })
    const json = await response.json()
    return {ok: response.ok, json: json}
  })

  ipcMain.handle('use-bp', async(_, use) => {
    response = await fetch(URL + '/use-bp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify ({
        use:use
      })
    })
    const json = await response.json()
    return {ok: response.ok, json: json}
  })
}