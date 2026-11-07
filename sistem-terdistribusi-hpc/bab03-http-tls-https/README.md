# Bab 3 -- HTTP, TLS, dan HTTPS

| Kode di buku | Berkas | Cara menjalankan |
|---|---|---|
| Kode 3.2 | `http_mentah.py` | `python3 http_mentah.py example.com` |
| Kode 3.3 | `klien_httpx.py` | `pip install -r requirements.txt && python3 klien_httpx.py` |
| Kode 3.4 | `java-klien/KlienHttp.java` | `java java-klien/KlienHttp.java` (JDK 11+, disarankan 21) |
| Kode 3.5 | `ukur_versi.sh` | `./ukur_versi.sh https://www.cloudflare.com/ 10` |
| Kode 3.6 | `lihat_sertifikat.sh` | `./lihat_sertifikat.sh www.google.com` |
| Kode 3.7 | `go-https/` | `mkcert -install && mkcert localhost 127.0.0.1` di folder itu, lalu `go run .` |
| Kode 3.8 | `go-mtls/` | `./buat_sertifikat.sh`, `go run . server`, lalu di terminal lain `go run . klien` dan `go run . klien-tanpa-sertifikat` |
| Kode 3.9 | `nginx/nginx.conf` | contoh konfigurasi; sesuaikan alamat upstream dan sertifikat |

Kode 3.1 (anatomi request/response) hanya teks dan dapat dicoba dengan `nc example.com 80`.
`ukur_versi.sh` membutuhkan curl yang dibangun dengan dukungan HTTP/3 untuk baris `--http3`.
