# Bab 1 -- Sistem Terdistribusi 101

Contoh kode pendamping Bab 1 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Kode di buku | Berkas | Cara menjalankan |
|---|---|---|
| Kode 1.1 | `hitung_janji.py` | `python3 hitung_janji.py` (tanpa dependensi) |
| Kode 1.2 | `go-latensi/main.go` | `cd go-latensi && go run .` (Go 1.22+) |
| Kode 1.3 | `pekko-penghitung/` | `cd pekko-penghitung && sbt run` (JDK 17/21, sbt) |
| Kode 1.4 | `gil_demo.py` | `python3 gil_demo.py`; bandingkan dengan Python free-threaded bila ada |
| Kode 1.5 | `ukur_latency.sh` | `./ukur_latency.sh` (butuh `ping`, `curl`, `traceroute`) |

Catatan:
- `hitung_janji.py` juga mencetak downtime per tahun dan contoh MTBF/MTTR dari subbab 1.3.2.
- Versi Pekko dan Scala pada `build.sbt` adalah versi stabil saat buku ditulis; naikkan bila perlu.
