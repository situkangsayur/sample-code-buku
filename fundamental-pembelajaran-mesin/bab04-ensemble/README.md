# Bab 4 - Ensemble

Contoh kode untuk Bab 4 buku *Fundamental Pembelajaran Mesin*. Sebagian besar contoh memakai data
Breast Cancer Wisconsin bawaan scikit-learn (lihat `data.py`), sehingga tidak perlu mengunduh apa pun.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `data.py` | - | Memuat data dan membagi latih/uji |
| `rf_oob.py` | Kode 4.1 | OOB error random forest terhadap jumlah pohon |
| `importance.py` | Kode 4.2 | MDI dibandingkan dengan permutation importance |
| `adaboost_numpy.py` | Kode 4.3 | AdaBoost dengan decision stump dari nol (contoh 10 titik) |
| `boosting_sklearn.py` | Kode 4.4 | AdaBoost dan gradient boosting di scikit-learn |
| `xgboost_early_stopping.py` | Kode 4.5 | XGBoost dengan early stopping |
| `voting_stacking.py` | Kode 4.6 | Voting dan stacking |
| `rust-bagging/` | Kode 4.7 | Bagging dengan stump dan suara terbanyak dalam Rust |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python rf_oob.py
python importance.py
python adaboost_numpy.py
python boosting_sklearn.py
python xgboost_early_stopping.py
python voting_stacking.py

cd rust-bagging && cargo run --release
```
