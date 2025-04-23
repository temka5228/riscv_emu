const { contentBridge, ipcRenderer, contextBridge } = require('electron/renderer')

contextBridge.exposeInMainWorld('riscvAPI', {
    loadFile: async (binaryString, address) => {
        return await ipcRenderer.invoke('load-file', binaryString, address)
    },
    startEmulation: async (address) => {
       return await ipcRenderer.invoke('run', address)
    },
    //getState: () => fetch('http://localhost:8000/state').then(res => console.log(res.json())),
    getRegisters: async () => {
        return await ipcRenderer.invoke('get-registers')
    },
    getMemory: async () => {
        return await ipcRenderer.invoke('get-memory')
    },
    decodeProgramm: async () => {
        return await ipcRenderer.invoke('decode')
    },
    setStartAddress: async (address) => {
        return await ipcRenderer.invoke('set-address', address)
    },
    setMemorySize: async (size) => {
        return ipcRenderer.invoke('set-memory', size)
    },

    onConsoleOutput: (callback) => {
        ipcRenderer.on('console-output', (_, data) => callback(data))
    }
})