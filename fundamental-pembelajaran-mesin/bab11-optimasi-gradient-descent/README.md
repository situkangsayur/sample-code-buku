# Bab 11 - Belajar sebagai Optimasi: Loss Function dan Gradient Descent

Kode pendamping buku *Fundamental Pembelajaran Mesin* (Hendri Karisma dan Hairul Umam), Bab 11.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `gd_numpy.py` | Gradient descent dari nol vs persamaan normal, uji batas learning rate | Kode 11.1 |
| `gd_rust/` | Gradient descent regresi linier satu fitur dalam Rust (tanpa crate) | Kode 11.2 |
| `sgd_minibatch.py` | Mini-batch SGD dengan cosine annealing pada data sintetis | Kode 11.3 |
| `ridge_lasso.py` | Ridge bentuk tertutup (NumPy) dan perbandingan ridge/lasso scikit-learn | Kode 11.4 |
| `logreg_numpy.py` | Regresi logistik dari nol pada data breast cancer Wisconsin | Kode 11.5 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python gd_numpy.py
python sgd_minibatch.py
python ridge_lasso.py
python logreg_numpy.py

cd gd_rust && cargo run --release
```
