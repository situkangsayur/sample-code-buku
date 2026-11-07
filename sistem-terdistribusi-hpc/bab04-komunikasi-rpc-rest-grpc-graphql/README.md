# Bab 4 - Komunikasi Antar Layanan: RPC, REST, gRPC, dan GraphQL

Contoh kode untuk Bab 4 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `java-rmi/` | Antarmuka `Katalog`, `ServerKatalog`, `KlienKatalog` dengan Java RMI (sejarah) | Kode 4.1 |
| `go-katalog/rest/main.go` | Layanan katalog REST: Problem Details (RFC 9457), ETag + `If-None-Match`, `PUT` dengan `If-Match` (optimistic concurrency), cursor pagination, token bucket | Kode 4.2, 4.4, Algoritma 4.1 |
| `go-katalog/openapi.yaml` | Kontrak OpenAPI 3.1 untuk layanan REST di atas | Kode 4.3 |
| `go-katalog/proto/katalog/v1/katalog.proto` | Kontrak Protobuf dengan empat mode panggilan | Kode 4.5 |
| `go-katalog/gen/katalogv1/` | Kode Go hasil `buf generate` (jangan diedit manual) | - |
| `go-katalog/grpcserver/main.go` | Server gRPC: unary, server/client/bidirectional streaming, interceptor `authLog`, health check, reflection | Kode 4.6, 4.8 |
| `go-katalog/grpcklien/main.go` | Klien gRPC dengan deadline 300 ms, metadata, dan contoh mode streaming | Kode 4.7 |
| `go-katalog/grpcklien/service_config.json` | Service config: timeout dan retry policy | Kode 4.9 |
| `go-katalog/coba_grpc.sh` | `grpcurl`, health check, `buf lint`, `buf breaking` | Kode 4.10 |
| `rust-tonic-klien/` | Klien gRPC Rust (`tonic`) dari `.proto` yang sama | Kode 4.12 |
| `graphql/dataloader.py` | DataLoader mini dengan `asyncio` dan perbandingan resolver naif (1 + N query) vs DataLoader (2 query) | Kode 4.15, Algoritma 4.2 |
| `go-sse/main.go` | Server SSE dengan hub siaran, heartbeat, dan halaman `EventSource` | Kode 4.17 |
| `go-retry/main.go` | Retry dengan exponential backoff, full jitter, dan deadline terhadap server palsu | Kode 4.19, Algoritma 4.3 |
| `idempotency/bayar.py` | Idempotency key dengan transaksi SQLite, termasuk uji tiga thread | Kode 4.20, Algoritma 4.4 |
| `ukur/uji_rest.js`, `ukur/uji_rest.sh`, `ukur/uji_grpc.sh` | Uji beban REST (k6) dan gRPC (`ghz`) | Kode 4.21 |

## Kebutuhan

- Go 1.22 atau lebih baru (pola router `GET /v1/produk/{id}` dan `math/rand/v2`).
- JDK 11 atau lebih baru untuk `java-rmi/`.
- Rust stabil + Cargo untuk `rust-tonic-klien/` (protoc ikut terunduh lewat crate `protoc-bin-vendored`).
- Python 3.10+ untuk `graphql/` dan `idempotency/` (hanya pustaka standar).
- Opsional: `buf`, `grpcurl`, `ghz`, dan k6 (program tersendiri, bukan paket npm).

## Menjalankan

```bash
# Java RMI (Kode 4.1)
cd java-rmi
make server            # terminal 1
make klien             # terminal 2 -> Kopi

# Layanan katalog Go (REST dan gRPC memakai data dan logika yang sama)
cd go-katalog
go run ./rest          # REST di :8080 (PORT=18080 bila 8080 sudah terpakai)
go run ./grpcserver    # gRPC di :50051
go run ./grpcklien     # -> Kopi 25000
go run ./grpcklien -id 99              # NOT_FOUND
go run ./grpcklien -mode pantau -n 3   # server streaming
go run ./grpcklien -mode impor         # client streaming
go run ./grpcklien -mode tawar         # bidirectional streaming
./coba_grpc.sh                         # butuh grpcurl dan buf

# membuktikan DEADLINE_EXCEEDED: beri jeda buatan 400 ms di server
JEDA=400ms go run ./grpcserver
go run ./grpcklien     # -> terlalu lambat, pakai data cadangan

# REST
curl -i localhost:8080/v1/produk/42
curl -i -H 'If-None-Match: "v1"' localhost:8080/v1/produk/42          # 304
curl -i -X PUT -H 'If-Match: "v1"' -d '{"nama":"Kopi Gayo","harga":27000}' \
     localhost:8080/v1/produk/42                                       # 200, ETag "v2"
curl -i -X PUT -H 'If-Match: "v1"' -d '{"nama":"Kopi","harga":1}' \
     localhost:8080/v1/produk/42                                       # 412
curl 'localhost:8080/v1/produk?limit=2'                                # cursor di "next"
RATE_LIMIT=1 go run ./rest   # nyalakan token bucket (r=10/detik, b=20), lalu kirim 30 request

# Membangkitkan ulang kode dari .proto (bila kontrak diubah)
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
make gen

# Klien Rust (server gRPC harus jalan)
cd rust-tonic-klien && cargo run

# Python
python graphql/dataloader.py
python idempotency/bayar.py --ulang

# SSE: buka http://localhost:8081/ di peramban, atau
cd go-sse && go run .
curl -N localhost:8081/v1/harga/42

# Retry
cd go-retry && go run .
go run . -gagal 9 -deadline 800ms      # deadline habis sebelum berhasil
```

## Eksperimen pengukuran (Subbab 4.10)

1. Jalankan `go run ./rest` dan `go run ./grpcserver` di mesin yang sama dengan data yang sama.
2. Jalankan alat ukur dari mesin atau inti CPU lain bila memungkinkan, agar tidak berebut CPU.
3. `ukur/uji_grpc.sh` dan `ukur/uji_rest.sh` menjalankan 10, 50, dan 200 pemanggil serentak,
   masing-masing tiga kali. Buang beberapa detik pertama (warm-up), laporkan median P50, P99,
   RPS, dan error rate.

## Catatan

- Klien `tonic` melaporkan deadline yang habis di sisi klien sebagai `Cancelled`
  ("Timeout expired"), bukan `DeadlineExceeded`. Karena itu `src/main.rs` memeriksa keduanya.
- Timeout `0.3s` di `service_config.json` berlaku untuk semua method layanan. Entri kedua
  per method menimpanya untuk method streaming yang memang berumur panjang.
- Health check dan reflection tidak memerlukan token. Pertimbangkan mematikan reflection di
  layanan publik.
