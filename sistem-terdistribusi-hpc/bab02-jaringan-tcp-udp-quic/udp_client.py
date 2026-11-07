"""Kode 2.7 (bawah): klien UDP dengan timeout, menghitung yang hilang."""
import socket
import statistics
import time

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.settimeout(0.5)  # wajib: datagram bisa hilang
hilang, rtt = 0, []
for i in range(100):
    t0 = time.perf_counter()
    c.sendto(f"ping {i}".encode(), ("127.0.0.1", 9001))
    try:
        c.recvfrom(2048)
        rtt.append((time.perf_counter() - t0) * 1000)
    except socket.timeout:
        hilang += 1
print(f"hilang: {hilang} dari 100")
if rtt:
    print(f"median RTT {statistics.median(rtt):.3f} ms, maks {max(rtt):.3f} ms")
