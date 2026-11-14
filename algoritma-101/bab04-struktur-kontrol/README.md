# Bab 4: Istilah Dasar dan Struktur Kontrol

Kode pendamping Bab 4 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `nilai_huruf.py` | rangkaian else-if | Algoritma 4.2 |
| `case_hari.py` | `match` sebagai case | Kode 4.1 |
| `collatz.py` | for (jumlah 1..n) dan while (Collatz) | Algoritma 4.3, 4.4 |
| `repeat_until.py` | repeat-until dengan `while True` dan `break` | Algoritma 4.5, Kode 4.5 |
| `break_continue.py` | break dan continue | Algoritma 4.6 |
| `lain/digit.pas` | repeat-until di Pascal | Kode 4.3 |
| `lain/digit.c`, `lain/Digit.java` | do-while di C dan Java | Kode 4.4 |
| `rust/src/bin/case_hari.rs` | `match` di Rust | Kode 4.2 |
| `rust/src/bin/repeat_until.rs` | `loop` dan `break` dengan nilai | Kode 4.6 |
| `rust/src/bin/nilai_huruf.rs` | else-if dan while di Rust | Algoritma 4.2, 4.4 |
| `rust/src/bin/break_continue.rs` | break, continue, dan label `'luar` | Algoritma 4.6 |

Menjalankan:

```
python3 nilai_huruf.py     # begitu pula berkas .py lain
cd lain && gcc -Wall -o digit digit.c && ./digit
cd lain && javac Digit.java && java Digit
cd lain && fpc digit.pas && ./digit      # butuh Free Pascal
cd rust && cargo test && cargo run --bin repeat_until
```

Nomor Kode dan Algoritma mengikuti urutan kemunculan di bab dan dapat bergeser bila naskah direvisi.
