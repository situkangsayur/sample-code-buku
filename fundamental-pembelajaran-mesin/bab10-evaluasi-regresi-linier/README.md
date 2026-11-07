# Bab 10 - Evaluasi Hipotesis dan Regresi Linier

Kode lengkap untuk Bab 10 buku *Fundamental Pembelajaran Mesin* (Hendri Karisma dan Hairul Umam).

| Berkas | Kode di buku | Isi |
|---|---|---|
| `selang_kepercayaan.py` | Kode 10.1 | sample error dan confidence interval |
| `metrik_klasifikasi.py` | Kode 10.2 | matriks konfusi, presisi, recall, F1, ROC-AUC, PR-AUC |
| `metrik_rust/` | Kode 10.3 | metrik dari matriks konfusi dalam Rust |
| `protokol_evaluasi.py` | Kode 10.4 | Pipeline + stratified k-fold tanpa kebocoran data |
| `banding_paired_ttest.py` | Kode 10.5 | paired t-test dua algoritma |
| `regresi_normal_equation.py` | Kode 10.6 | normal equation, R^2, R^2_adj, standard error |
| `regresi_rust/` | Kode 10.7 | regresi linier satu variabel dalam Rust |
| `diagnostik_vif.py` | Kode 10.8 | VIF pada data harga rumah sintetis |
| `evaluasi_regresi.py` | Kode 10.9 | RMSE/MAE/R^2 dengan 5-fold CV dan data uji |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python selang_kepercayaan.py
python metrik_klasifikasi.py
python protokol_evaluasi.py
python banding_paired_ttest.py
python regresi_normal_equation.py
python diagnostik_vif.py
python evaluasi_regresi.py

cd metrik_rust && cargo run
cd ../regresi_rust && cargo run
```

Data yang dipakai adalah data bawaan scikit-learn (`load_breast_cancer`, `load_diabetes`) atau
dibangkitkan di dalam skrip, sehingga tidak perlu unduhan.
