# Bab 38: Algoritma di Streaming dan Cache

| File | Isi | Kaitan di buku |
|---|---|---|
| `kafka_log.py` | log append-only berpartisi, offset, consumer group, rebalance, queue klasik pembanding | Subbab 37.1-37.2 |
| `skip_list.py` | skip list (Pugh 1990) dan sorted set hash + skip list ala Redis | Subbab 37.3 |
| `hyperloglog.py` | HyperLogLog sederhana dan penggabungan | Subbab 37.3 |
| `consistent_hash.py` | ring consistent hashing dengan virtual node, dibandingkan dengan hash mod N | Subbab 37.4 |
| `token_bucket.py` | token bucket dan fixed window | Subbab 37.5 |
| `rust/src/bin/*.rs` | `partitioned_log`, `consistent_hash`, `token_bucket`, `hyperloglog` | versi Rust dari pseudocode yang sama |

Semua hash memakai FNV-1a 64 bit (ditambah finalizer splitmix64) yang ditulis sendiri,
sehingga Python dan Rust memberi angka yang sama.

Menjalankan:

```
python3 kafka_log.py   # begitu pula berkas .py lain
cd rust && cargo test && cargo run --bin consistent_hash
```
