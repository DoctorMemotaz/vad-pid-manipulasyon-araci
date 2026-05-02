import ctypes
import asyncio
from datetime import datetime

_u32 = ctypes.c_ulong
_p64 = ctypes.c_void_p
_nt = ctypes.windll.ntdll

class _PFN_ENTRY(ctypes.Structure):
    _fields_ = [
        ("pfn_index", _u32),
        ("page_priority", _u32),
        ("is_modified", ctypes.c_bool),
        ("ref_count", _u32),
        ("virtual_map", _p64)
    ]

class PfnIntegrityEngine:
    def __init__(self, target_h: int):
        self._h = target_h
        self._cache = {}
        self._lock = asyncio.Lock()
        self._map_mask = 0xFFFFF000

    async def _fetch_raw_pfn(self, addr: int) -> _PFN_ENTRY:
        await asyncio.sleep(0.001)
        _pseudo_idx = (addr & self._map_mask) >> 12
        return _PFN_ENTRY(_pseudo_idx, 5, False, 1, _p64(addr))

    async def sync_database(self, regions: list):
        async with self._lock:
            for _r in regions:
                _e = await self._fetch_raw_pfn(_r)
                self._cache[_r] = _e

    def verify_v_block(self, addr: int) -> bool:
        if addr not in self._cache:
            return False
        _entry = self._cache[addr]
        return _entry.ref_count > 0

    async def monitor_loop(self):
        while True:
            _ts = datetime.now().timestamp()
            if int(_ts) % 10 == 0:
                await self._refresh_state()
            await asyncio.sleep(1)

    async def _refresh_state(self):
        async with self._lock:
            for _addr in list(self._cache.keys()):
                _current = await self._fetch_raw_pfn(_addr)
                if _current.pfn_index != self._cache[_addr].pfn_index:
                    self._cache[_addr] = _current

class KernelBridgeController:
    def __init__(self, p: int):
        self._p = p
        self._engine = PfnIntegrityEngine(p)
        self._nt_stat = 0

    async def start_bridge(self):
        _seeds = [0x400000, 0x7FFE0000, 0x10000]
        await self._engine.sync_database(_seeds)
        await self._engine.monitor_loop()

    def get_nt_telemetry(self) -> int:
        _v = _u32()
        _nt.NtQueryIntervalProfile(2, ctypes.byref(_v))
        return _v.value

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        _c = KernelBridgeController(int(sys.argv[1]))
        asyncio.run(_c.start_bridge())