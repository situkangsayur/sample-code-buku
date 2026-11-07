# Bab 10 - Melatih Jaringan Saraf secara Stabil

Kode pendamping buku *Fundamental Pembelajaran Mesin* (Hendri Karisma), Bab 10.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `init_eksperimen.py` | Simpangan baku aktivasi 10 lapisan ReLU: acak kecil vs Xavier vs He (data Gambar 10.2) | Kode 10.1 |
| `optimizer_numpy.py` | GD, momentum, RMSProp, Adam dari nol pada data jam belajar (data Gambar 10.3) | Kode 10.2 |
| `adam_rust/` | Optimizer Adam dalam Rust tanpa crate | Kode 10.3 |
| `tuning_optuna.py` | Penyetelan hyperparameter dengan Optuna (TPE + median pruning) | Kode 10.4 |
| `eksperimen_fashion_mlp.py` | Skenario pembuka bab (He + AdamW vs acak kecil + SGD) dan Tabel pembanding E01-E03, tanpa torchvision | pembuka bab, Tabel 10.5 |
| `latih_fashion.py` | Resep lengkap: seed, He init, BN, dropout, AdamW, cosine, augmentasi, early stopping, log CSV | Kode 10.5-10.7 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python init_eksperimen.py
python optimizer_numpy.py
python latih_fashion.py --epoch 30 --lr 1e-3 --dropout 0.3 --seed 42
python tuning_optuna.py          # 30 trial, cukup lama di CPU

cd adam_rust && cargo run --release
```

`latih_fashion.py` mengunduh Fashion-MNIST ke `data/`, menulis `log_pelatihan.csv`
(untuk menggambar kurva) dan `model_terbaik.pt` (checkpoint early stopping).
