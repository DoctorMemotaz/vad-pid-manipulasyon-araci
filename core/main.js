const { app, BrowserWindow, ipcMain, shell } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let _mainWin;
let _pyHandle = null;

function _createFrame() {
    const _v_ico = app.isPackaged 
        ? path.join(process.resourcesPath, 'assets/icon.ico') 
        : path.join(__dirname, '../assets/icon.ico');

    _mainWin = new BrowserWindow({
        width: 440,
        height: 620,
        frame: false,
        resizable: false,
        icon: _v_ico,
        backgroundColor: '#0d0d0f',
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'bridge.js')
        }
    });

    const _targetUI = app.isPackaged 
        ? path.join(__dirname, 'index.html') 
        : path.join(__dirname, '../view/index.html');
        
    _mainWin.loadFile(_targetUI);
}

const _killSrv = () => {
    if (_pyHandle) {
        try {
            _pyHandle.kill();
            _pyHandle = null;
        } catch (e) {}
    }
};

ipcMain.on('v_call', (e, args) => {
    if (args.type === 'engage') {
        const _srvPath = app.isPackaged 
            ? path.join(process.resourcesPath, 'srv_bin/kernel.exe')
            : path.join(__dirname, '../engine/srv.py');

        const _exec = app.isPackaged ? _srvPath : 'python';
        const _params = app.isPackaged ? [args.pid] : [_srvPath, args.pid];

        _pyHandle = spawn(_exec, _params, { windowsHide: true });
        _pyHandle.stdout.on('data', (d) => {
            if (_mainWin) _mainWin.webContents.send('v_sync', d.toString());
        });
    } else {
        _killSrv();
    }
});

ipcMain.on('v_link', (e, u) => shell.openExternal(u));
ipcMain.on('v_close', () => {
    _killSrv();
    app.quit();
});

app.on('ready', _createFrame);

app.on('before-quit', () => {
    _killSrv();
});

app.on('will-quit', () => {
    _killSrv();
});

app.on('window-all-closed', () => {
    _killSrv();
    if (process.platform !== 'darwin') app.quit();
});

process.on('exit', () => {
    _killSrv();
});