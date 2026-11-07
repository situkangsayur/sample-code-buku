# Bab 6 - Gaussian Mixture Model dan Algoritma EM

Contoh kode untuk Bab 6 buku *Fundamental Pembelajaran Mesin*. Semua angka keluaran
yang dicetak di buku berasal dari skrip-skrip ini (NumPy 2.4, SciPy 1.16, scikit-learn 1.7).

| Berkas | Kode di buku | Isi |
|---|---|---|
| `data_nasabah.py` | - | Pembangkit data sintetis segmentasi nasabah (500 nasabah, 3 segmen, 2 fitur) |
| `gaussian_mle.py` | Kode 6.1 | Log-densitas Gaussian multivariat (Cholesky) dan MLE satu Gaussian |
| `em_tangan_1d.py` | - | Contoh hitungan tangan EM 1D dua komponen, mencetak iterasi 1 dan 2 |
| `gmm_numpy.py` | Kode 6.2 | EM untuk GMM dari nol (kovarians penuh, log-sum-exp, reg_covar), inisialisasi acak vs K-Means, sepuluh seed |
| `gmm_sklearn.py` | Kode 6.3 | `GaussianMixture`: parameter, soft assignment nasabah baru, ARI, Iris (GaussianNB vs GMM) |
| `gmm_bic.py` | Kode 6.4 | BIC dan AIC untuk K = 1..6 dan empat bentuk kovarians |
| `gmm_anomali.py` | Kode 6.5 | Deteksi anomali dengan `score_samples` dan ambang persentil 1 |
| `campuran_bernoulli.py` | - | EM untuk campuran Bernoulli pada data biner pemakaian layanan (Bishop Subbab 9.3.3) |
| `singularitas.py` | - | Log-likelihood naik tanpa batas saat varians satu komponen mengecil; efek reg_covar |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python em_tangan_1d.py
python gaussian_mle.py
python gmm_numpy.py
python gmm_sklearn.py
python gmm_bic.py
python gmm_anomali.py
python singularitas.py
python campuran_bernoulli.py
```

Data nasabah bersifat sintetis (dibangkitkan dari tiga Gaussian dengan `seed=6`), bukan data bank nyata.
