let _isRunning = false;
const _btn = document.getElementById('v_toggle'), _inp = document.getElementById('v_pid_input'), _log = document.getElementById('v_terminal');
_btn.onclick = () => {
    if (!_isRunning) {
        if (!_inp.value) return;
        _v_core.tx('v_call', { type: 'engage', pid: _inp.value });
        _isRunning = true;
    } else { _stopLogic(); }
};
_v_core.rx('v_sync', (raw) => {
    const _s = raw.trim();
    if (_s.includes("SIGNAL_FAIL")) { _pushLog("HATA: PID bulunamadı veya erişim reddedildi."); _stopLogic(); }
    else if (_s.includes("SIGNAL_LOCKED")) { 
        _btn.innerText = 'KORUMAYI DURDUR'; _btn.classList.add('active'); 
        _pushLog("BAŞARILI: VAD manipülasyonu aktif."); 
    }
});
function _stopLogic() { 
    _v_core.tx('v_call', { type: 'disengage' }); 
    _btn.innerText = 'KORUMAYI ETKİNLEŞTİR'; _btn.classList.remove('active'); 
    _isRunning = false; 
}
document.getElementById('v_dev_btn').onclick = (e) => { e.preventDefault(); _v_core.ext('https://github.com/doctormemotaz'); };
document.getElementById('v_exit').onclick = () => _v_core.tx('v_close');
function _pushLog(m) { const d = document.createElement('div'); d.innerText = `[${new Date().toLocaleTimeString()}] > ${m}`; _log.appendChild(d); _log.scrollTop = _log.scrollHeight; }