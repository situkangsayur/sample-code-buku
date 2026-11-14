# Bab 16: Linked List

| File | Isi | Kaitan di buku |
|---|---|---|
| `singly_linked_list.py` | Single linked list: push_front, push_back, find, insert_after, delete, reverse | Algoritma 16.1-16.3; Kode 16.1, 16.2 |
| `doubly_linked_list.py` | Double linked list dengan dua sentinel | Algoritma 16.4 |
| `josephus.py` | Masalah Josephus dengan circular linked list dan rumus rekursif | Algoritma 16.5; Kode 16.3; Tabel 16.2 |
| `cache_benchmark.py` | Menjumlahkan list vs linked list di Python | Subbab 16.6 |
| `rust/src/bin/singly.rs` | `List<T>` dengan `Option<Box<Node<T>>>`, Drop iteratif | Kode 16.4 |
| `rust/src/bin/josephus.rs` | Josephus dengan linked list berbasis indeks | Subbab 16.5 |
| `rust/src/bin/cache_bench.rs` | Vec vs LinkedList vs node berurutan/acak | Tabel 16.4 |

Menjalankan:

```
for f in singly_linked_list doubly_linked_list josephus cache_benchmark; do python3 $f.py; done
cd rust && cargo test && cargo run --bin singly && cargo run --bin josephus
cargo run --release --bin cache_bench
```

Angka waktu bergantung mesin.
