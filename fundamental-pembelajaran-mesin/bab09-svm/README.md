# Bab 9 - Support Vector Machine

Kode lengkap untuk Bab 9 buku *Fundamental Pembelajaran Mesin* (Hendri Karisma dan Hairul Umam).

| Berkas | Kode di buku | Isi |
|---|---|---|
| `svm_enam_titik.py` | Kode 9.1 | SVM linier pada enam titik: w, b, support vector, alpha |
| `kernel_cek.py` | Kode 9.2 | pemeriksaan kernel trick dan peluruhan RBF |
| `svm_grid_search.py` | Kode 9.3 | grid search C dan gamma, dengan dan tanpa scaling |

Kode naive Bayes yang dibandingkan dengan SVM di bab ini ada di folder
`bab05-bayesian-naive-bayes/`.

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python svm_enam_titik.py
python kernel_cek.py
python svm_grid_search.py
```

Semua data kecil ditulis langsung di dalam kode; `svm_grid_search.py` membangkitkan data dengan
`make_circles`.
