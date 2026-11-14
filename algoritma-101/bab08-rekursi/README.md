# Bab 8: Rekursi

Kode pendamping Bab 8 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `faktorial_rek.py` | faktorial rekursif, `RecursionError` untuk n = 5000, jumlah digit, pangkat rekursif | Algoritma 8.1, Kode 8.1, Subbab 8.5 |
| `hanoi.py` | Menara Hanoi | Algoritma 8.2 |
| `fibonacci.py` | FibRek dengan penghitung, memoization, FibIter, rumus Binet, pengukuran waktu | Algoritma 8.3--8.4, Kode 8.2, Tabel 8.1 |
| `rust/src/bin/fibonacci.rs` | FibIter, `checked_add`, FibRek dengan penghitung | Kode 8.3 |
| `rust/src/bin/hanoi.rs` | Menara Hanoi di Rust | Latihan 9 |
| `rust/src/bin/faktorial_rek.rs` | faktorial rekursif, rekursi dalam di thread dengan stack besar | Subbab 8.3 |

Menjalankan:

```
python3 faktorial_rek.py
python3 hanoi.py
python3 fibonacci.py        # mencetak waktu fib_rek(30) dan fib_rek(35), beberapa detik
cd rust && cargo test && cargo run --bin fibonacci && cargo run --bin hanoi && cargo run --bin faktorial_rek
```

Waktu di Tabel 8.1 diukur dengan Python 3.12.3 pada Intel Xeon E5-2697 v4; di mesin lain angkanya
berbeda, tetapi perbandingan waktu n = 35 terhadap n = 30 tetap sekitar 11 kali.
