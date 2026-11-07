# Bab 2 -- Jaringan: IP, Socket, TCP, UDP, dan QUIC

| Kode di buku | Berkas | Cara menjalankan |
|---|---|---|
| Kode 2.1 | `dig.sh` | `./dig.sh` (butuh `dig`, paket dnsutils/bind-tools) |
| Kode 2.2 | `c-echo/echo_server.c` | `cd c-echo && make && ./echo_server` |
| Kode 2.3 | `go-echo/main.go` | `cd go-echo && go run .` |
| Kode 2.4 | `tcp_client.py` | `python3 tcp_client.py 100` (server di :9000 harus jalan) |
| Kode 2.5 | `rust-echo/` | `cd rust-echo && cargo run --release` |
| Kode 2.6 | `framing/framing.py` | `python3 framing/server.py` lalu `python3 framing/client.py` |
| Kode 2.7 | `udp_server.py`, `udp_client.py` | `python3 udp_server.py` lalu `python3 udp_client.py` |
| Kode 2.8, 2.9 | `amati.sh` | `./amati.sh info`, `./amati.sh jelek`, `./amati.sh pulih` |
| (hitungan) | `hitung_tcp.py` | `python3 hitung_tcp.py`: RTO, BDP, Mathis, waktu transfer |

Semua server memakai port 9000 (TCP), 9001 (UDP), atau 9100 (TCP berframing); jalankan satu
server TCP pada satu waktu. Eksperimen `netem` sebaiknya di VM Linux; jangan lupa `./amati.sh pulih`.
