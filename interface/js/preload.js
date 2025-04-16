const { contentBridge, ipcRenderer, contextBridge } = require('electron/renderer')

contextBridge.exposeInMainWorld('riscvAPI', {
    selectFile: () => ipcRenderer.invoke('select-file'),
    startEmulation: (binaryString, startPosition) => {
        console.log('int preload start emulator')
        ipcRenderer.invoke('start-emulation', binaryString, startPosition)},
    getState: () => fetch('http://localhost:8000/state').then(res => console.log(res.json()))

})