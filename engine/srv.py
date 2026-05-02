import ctypes
import sys
import time

_kernel = ctypes.windll.kernel32

class _VAD_STRUCTURE(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize", ctypes.c_size_t),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong)
    ]

_kernel.VirtualQueryEx.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(_VAD_STRUCTURE), ctypes.c_size_t]
_kernel.VirtualProtectEx.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
_kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]

def _verify_proc(p):
    _h = _kernel.OpenProcess(0x1000, False, int(p))
    if _h:
        _kernel.CloseHandle(_h)
        return True
    return False

def _apply_mask(pid):
    _h_proc = _kernel.OpenProcess(0x1F0FFF, False, int(pid))
    if not _h_proc: return False
    
    _cursor = 0
    _old_p = ctypes.c_ulong()
    _mbi = _VAD_STRUCTURE()
    
    while _cursor < 0x7FFFFFFFFFFF:
        if _kernel.VirtualQueryEx(_h_proc, ctypes.c_void_p(_cursor), ctypes.byref(_mbi), ctypes.sizeof(_mbi)):
            if _mbi.Protect in [0x20, 0x40, 0x80]:
                _kernel.VirtualProtectEx(_h_proc, ctypes.c_void_p(_mbi.BaseAddress), _mbi.RegionSize, 0x100, ctypes.byref(_old_p))
            _cursor += _mbi.RegionSize
        else:
            _cursor += 0x1000
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        _pid = sys.argv[1]
        if not _verify_proc(_pid):
            print("SIGNAL_FAIL")
            sys.stdout.flush()
            sys.exit(1)
        if _apply_mask(_pid):
            print(f"SIGNAL_LOCKED_{_pid}")
            sys.stdout.flush()
            while True: time.sleep(1)