const { contentBridge, ipcRenderer, contextBridge } = require('electron/renderer')

contextBridge.exposeInMainWorld('riscvAPI', {
    loadFile: async (binaryString, address) => {
        return await ipcRenderer.invoke('load-file', binaryString, address)
    },
    startEmulation: async (address) => {
        return await ipcRenderer.invoke('run', address)
    },
    stop: async () => {
        ipcRenderer.invoke('stop')
    },
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
    },
    selectPredictor: async (name) => {
        return await ipcRenderer.invoke('select-predictor', name)
    },
    useBranch: async (use) => {
        return await ipcRenderer.invoke('use-bp', use)
    },
    selectModel: async (model) => {
        return await ipcRenderer.invoke('model-select', model)
    }

})