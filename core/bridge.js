const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('_v_core', {
    tx: (c, d) => ipcRenderer.send(c, d),
    rx: (c, f) => ipcRenderer.on(c, (e, ...a) => f(...a)),
    ext: (u) => ipcRenderer.send('v_link', u)
});