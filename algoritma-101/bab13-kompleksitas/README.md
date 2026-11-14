# Bab 13: Kompleksitas Algoritma dan Notasi Asimtotik

| File | Isi | Kaitan di buku |
|---|---|---|
| `count_pairs.py` | CountPairs naif dengan penghitung langkah, versi sort + dua penunjuk, tiga kasus linear search, pengukuran waktu | Algoritma 13.1, 13.2; Kode 13.1; Tabel 13.2 |
| `growth_table.py` | Nilai kelas pertumbuhan dan taksiran waktu pada 10^8 operasi/detik | Tabel 13.4, 13.5 |
| `rust/src/bin/count_pairs.rs` | CountPairs dan linear search di Rust, dengan `#[test]` | Kode 13.2 |
| `rust/src/bin/growth_table.rs` | Nilai fungsi pertumbuhan | Tabel 13.4 |

Menjalankan:

```
python3 count_pairs.py
python3 growth_table.py
cd rust && cargo test && cargo run --bin count_pairs && cargo run --bin growth_table
```

Angka waktu bergantung mesin.
