"""Klien berframing: kirim pesan 10 B, 1 KB, dan 1 MB lalu cek balasan utuh."""
import os
import socket

from framing import kirim_pesan, terima_pesan

with socket.create_connection(("127.0.0.1", 9100), timeout=5) as s:
    for ukuran in (10, 1024, 1024 * 1024):
        data = os.urandom(ukuran)
        kirim_pesan(s, data)
        balas = terima_pesan(s)
        print(f"{ukuran:8d} byte -> utuh: {balas == data}")
