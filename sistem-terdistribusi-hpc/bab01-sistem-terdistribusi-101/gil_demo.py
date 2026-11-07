"""Kode 1.4: efek GIL -- thread vs proses untuk pekerjaan CPU.

Jalankan: python3 gil_demo.py
Bandingkan juga dengan Python free-threaded (mis. python3.14t) bila tersedia.
"""
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def hitung(n):  # pekerjaan CPU murni
    s = 0
    for i in range(n):
        s += i * i
    return s


def tidur(_):  # pekerjaan "I/O": GIL dilepas saat menunggu
    time.sleep(1)


def ukur(Executor, nama, fungsi, argumen):
    t0 = time.perf_counter()
    with Executor(max_workers=4) as ex:
        list(ex.map(fungsi, argumen))
    print(f"{nama:22s} {time.perf_counter() - t0:.2f} detik")


if __name__ == "__main__":
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print("GIL aktif:", gil)
    ukur(ThreadPoolExecutor, "CPU, 4 thread", hitung, [5_000_000] * 4)
    ukur(ProcessPoolExecutor, "CPU, 4 proses", hitung, [5_000_000] * 4)
    ukur(ThreadPoolExecutor, "sleep, 4 thread", tidur, range(4))
