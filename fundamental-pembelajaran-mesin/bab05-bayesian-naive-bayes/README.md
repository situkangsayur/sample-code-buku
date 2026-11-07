# Bab 5 - Bayesian Learning dan Naive Bayes

Kode lengkap untuk Bab 5 buku *Fundamental Pembelajaran Mesin* (Hendri Karisma dan Hairul Umam).

| Berkas | Kode di buku | Isi |
|---|---|---|
| `bayes_penyakit.py` | Kode 5.1 | teorema Bayes pada uji penyakit langka, pembaruan keyakinan bertahap |
| `naive_bayes_manual.py` | Kode 5.2 | naive Bayes multinomial dari nol, Laplace, log-sum-exp |
| `naive_bayes_sklearn.py` | Kode 5.3 | CountVectorizer + MultinomialNB, kata dengan bukti terkuat |
| `nb_rust/` | Kode 5.4 | naive Bayes multinomial dalam Rust |
| `playtennis_nb.py` | (contoh hitungan) | naive Bayes kategorikal PlayTennis, dengan dan tanpa Laplace |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bayes_penyakit.py
python naive_bayes_manual.py
python naive_bayes_sklearn.py
python playtennis_nb.py

cd nb_rust && cargo run
```

Semua data kecil ditulis langsung di dalam kode.
