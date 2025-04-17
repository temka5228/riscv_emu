const { contentBridge, ipcRenderer, contextBridge } = require('electron/renderer')

contextBridge.exposeInMainWorld('riscvAPI', {
    loadFile: async (binaryString, startPosition) => {
        return await ipcRenderer.invoke('load-file', binaryString, startPosition)
    },
    startEmulation: async () => {
       return await ipcRenderer.invoke('run')
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
    }
})