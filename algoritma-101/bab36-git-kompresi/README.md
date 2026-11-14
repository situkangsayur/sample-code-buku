# Bab 36: Algoritma di Git dan Kompresi

Kode lengkap Bab 36 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `git_object.py` | id blob dan tree Git (SHA-1), dibandingkan dengan `git hash-object` dan `git write-tree`; membaca object loose (zlib) | Algoritma 36.1, Kode 36.1 |
| `merkle.py` | Merkle root, bukti keanggotaan, verifikasi, perbandingan dua replica | Algoritma 36.2, Kode 36.3 |
| `delta.py` | encoder dan decoder delta copy/insert ala packfile | Algoritma 36.3, Contoh delta |
| `packfile_demo.sh` | tiga versi satu file, `git gc`, lalu `git verify-pack -v` | Tabel 36.2, Gambar 36.2 |
| `lz77_huffman.py` | LZ77 naif, panjang kode Huffman, perbandingan zlib dan zstd (bila CLI `zstd` ada) | Contoh LZ77, Tabel 36.3 |
| `rust/src/lib.rs` | SHA-1 (FIPS 180-4) tanpa crate luar dan `object_id` | Kode 36.2 |
| `rust/src/bin/blob_id.rs` | id blob `hello\n` | Kode 36.2 |
| `rust/src/bin/lz77.rs` | encoder dan decoder LZ77 | Kode 36.4 |

Cara menjalankan (Python 3.12, Git, opsional zstd CLI; diuji dengan Git 2.43.0 dan zstd 1.5.5):

```
python3 git_object.py
python3 merkle.py
python3 delta.py
python3 lz77_huffman.py
bash packfile_demo.sh
cd rust
cargo test
cargo run --bin blob_id
cargo run --bin lz77
```

SHA-1 di `rust/src/lib.rs` hanya untuk belajar. Untuk keperluan keamanan pakai library kriptografi yang sudah diaudit.
