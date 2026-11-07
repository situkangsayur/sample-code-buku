"""Kode 2.4: klien TCP yang mengukur RTT tingkat aplikasi.

Jalankan server dulu (go-echo atau c-echo), lalu: python3 tcp_client.py [jumlah]
"""
import statistics
import socket
import sys
import time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
alamat = ("127.0.0.1", 9000)
rtt = []
with socket.create_connection(alamat, timeout=2) as s:
    f = s.makefile("rwb")  # bungkus socket jadi berkas
    for i in range(N):
        t0 = time.perf_counter()
        f.write(f"halo {i}\n".encode())
        f.flush()
        balas = f.readline()  # tunggu satu baris utuh
        ms = (time.perf_counter() - t0) * 1000
        rtt.append(ms)
        if N <= 10:
            print(balas.decode().strip(), f"{ms:.3f} ms")
print(f"n={N} rata={statistics.mean(rtt):.3f} median={statistics.median(rtt):.3f} "
      f"maks={max(rtt):.3f} ms")
