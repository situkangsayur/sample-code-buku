# Bab 1 - Machine Learning 101

Contoh kode untuk Bab 1 buku *Fundamental Pembelajaran Mesin*.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `analitik_numerik.py` | Kode 1.1 | Regresi linier: normal equation vs gradient descent |
| `rust-gradient-descent/` | Kode 1.2 | Gradient descent satu dimensi dalam Rust |
| `ukur_waktu.py` | Kode 1.3 | Mengukur laju pertumbuhan O(n^2) vs O(n log n) |
| `split_data.py` | Kode 1.4 | Pembagian data latih/validasi/uji dan pemilihan kedalaman pohon |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python analitik_numerik.py
python ukur_waktu.py
python split_data.py

cd rust-gradient-descent && cargo run --release
```
