"""Kode 3.2: mengirim HTTP/1.1 langsung lewat socket TCP.

Jalankan: python3 http_mentah.py [host]
"""
import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "example.com"
permintaan = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"  # minta server menutup setelah menjawab
    "\r\n"                   # baris kosong = akhir header
)
with socket.create_connection((host, 80), timeout=5) as s:
    s.sendall(permintaan.encode("ascii"))
    jawaban = b""
    while potong := s.recv(4096):  # baca sampai server menutup
        jawaban += potong
kepala, _, badan = jawaban.partition(b"\r\n\r\n")
print(kepala.decode(errors="replace"))
print(f"... body {len(badan)} byte")
