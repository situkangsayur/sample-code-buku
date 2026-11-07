# Bab 6 - Concurrency dan Model Runtime

Contoh kode untuk Bab 6 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.
Prasyarat: JDK 21+, Go 1.22+, Rust (cargo), Python 3.12+, Node.js 20+, sbt (untuk Pekko).

| Folder/berkas | Isi | Kaitan di buku |
|---|---|---|
| `java/Balapan.java` | Race condition pada `n++` | Kode 6.1 |
| `java/Tambal.java` | synchronized, ReentrantLock, AtomicInteger + pengukuran | Kode 6.2 |
| `java/Deadlock.java` | Deadlock urutan lock terbalik dan perbaikan urutan global | Kode 6.3, 6.4 |
| `java/VirtualThreads.java` | Fixed thread pool vs virtual thread (Java 21) | Kode 6.5 |
| `java/SaldoBersama.java` | Soal saldo bersama: virtual thread + AtomicLong | Kode 6.17 |
| `go/goroutine` | goroutine, channel, WaitGroup | Kode 6.6 |
| `go/selecttimeout` | select + time.After, context.WithTimeout | Kode 6.7 |
| `go/workerpool` | Worker pool empat pekerja | Kode 6.8 |
| `go/saldo` | Soal saldo bersama: pemilik tunggal (channel) vs Mutex | Kode 6.18 |
| `pekko/` | Actor Penghitung bertipe + 1.000 pengirim (Apache Pekko, Java) | Kode 6.9 |
| `node/` | Event loop: I/O-bound, CPU-bound yang membekukan, worker_threads | Kode 6.12 |
| `python/asyncio_gather.py` | 100 tugas I/O bersamaan, jebakan memblokir loop, to_thread | Kode 6.13 |
| `python/gil_thread_process.py` | Efek GIL: thread vs process | Kode 6.16 |
| `rust/` | Tokio: banyak permintaan HTTP, spawn_blocking | Kode 6.15 |

## Menjalankan

```bash
# Java (tanpa build tool, Java 21+)
cd java
java Balapan.java            # ulangi beberapa kali
java Tambal.java 2; java Tambal.java 8; java Tambal.java 1000
java Deadlock.java macet     # menggantung 3 detik, lalu melapor; coba jstack <pid>
java Deadlock.java urut
java VirtualThreads.java
java SaldoBersama.java

# Go
cd go
go run ./goroutine
go run ./selecttimeout
go run ./workerpool
go run -race ./saldo && go run ./saldo && go run ./saldo mutex

# Pekko (Java + sbt)
cd pekko && sbt run

# Node.js
cd node && npm install && PORT=3999 npm start
# terminal lain:
curl localhost:3999/laporan-lambat &  curl -w "%{time_total}\n" localhost:3999/saldo?id=1
curl localhost:3999/laporan &         curl -w "%{time_total}\n" localhost:3999/saldo?id=1

# Python
python python/asyncio_gather.py
python python/gil_thread_process.py

# Rust
cd rust && cargo run --release -- https://example.com 50
```

## Praktikum "satu soal, tiga model" (Subbab 6.11)

Isi tabel berikut dari 5 kali jalan (laporkan median):

| Model | Benar? | Waktu median | Baris kode | Penjelasan |
|---|---|---|---|---|
| Java AtomicLong + virtual thread | | | | |
| Go channel (pemilik tunggal) | | | | |
| Go Mutex | | | | |
| Pekko actor | | | | |

Contoh hasil di satu laptop (Linux, 16 core): Java sekitar 14 ms, Go channel sekitar 580 ms,
Go Mutex sekitar 80 ms, Pekko sekitar 560 ms. Operasi "tambah satu" terlalu kecil untuk channel
dan actor; ongkos per pesan mendominasi.
