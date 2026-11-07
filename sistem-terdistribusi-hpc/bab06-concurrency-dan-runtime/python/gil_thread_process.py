"""Kode 6.16: thread untuk I/O, process untuk CPU di Python (efek GIL).

Pemakaian: python gil_thread_process.py
Bagian I/O memakai time.sleep sebagai pengganti jaringan agar dapat dijalankan offline.
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import sys, time


def tunggu_io(_):                     # I/O-bound: GIL dilepas saat menunggu
    time.sleep(0.5)
    return 1


def hitung(n):                        # CPU-bound: GIL menahan thread lain
    return sum(i * i for i in range(n))


def ukur(nama, ex_cls, fungsi, data):
    t = time.perf_counter()
    with ex_cls(8) as ex:
        list(ex.map(fungsi, data))
    print(f"{nama:28s}: {time.perf_counter() - t:5.2f} s")


if __name__ == "__main__":
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {sys.version.split()[0]}, GIL aktif: {gil}")
    ukur("I/O dengan 8 thread", ThreadPoolExecutor, tunggu_io, range(16))
    t = time.perf_counter(); [hitung(3_000_000) for _ in range(8)]
    print(f"{'CPU berurutan':28s}: {time.perf_counter() - t:5.2f} s")
    ukur("CPU dengan 8 thread (GIL)", ThreadPoolExecutor, hitung, [3_000_000] * 8)
    ukur("CPU dengan 8 process", ProcessPoolExecutor, hitung, [3_000_000] * 8)
