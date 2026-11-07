"""Server echo berframing: python3 server.py (port 9100)."""
import socket
import threading

from framing import kirim_pesan, terima_pesan


def layani(c):
    with c:
        try:
            while True:
                kirim_pesan(c, terima_pesan(c))
        except (ConnectionError, ValueError):
            pass


with socket.create_server(("0.0.0.0", 9100), reuse_port=True) as ln:
    print("server berframing di :9100")
    while True:
        c, _ = ln.accept()
        threading.Thread(target=layani, args=(c,), daemon=True).start()
