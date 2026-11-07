# Bab 3 - Decision Tree

Contoh kode untuk Bab 3 buku *Fundamental Pembelajaran Mesin*.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `playtennis.csv` | - | 14 contoh PlayTennis (Mitchell, 1997, Tabel 3.2) |
| `entropy_gain.py` | Kode 3.1 | Entropy, information gain, dan gain ratio dengan NumPy |
| `id3.py` | Kode 3.2 | ID3 rekursif dari nol dan prediksi hari baru |
| `rust-entropy/` | Kode 3.3 | Entropy dan information gain dalam Rust |
| `sklearn_playtennis.py` | Kode 3.4 | Pohon PlayTennis dengan scikit-learn dan `export_text` |
| `pruning_ccp.py` | Kode 3.5 | Memilih `ccp_alpha` dengan cross-validation |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python entropy_gain.py
python id3.py
python sklearn_playtennis.py
python pruning_ccp.py

cd rust-entropy && cargo run --release
```
