# Bab 8 - k-Nearest Neighbour dan K-Means

Kode lengkap untuk Bab 8 buku *Fundamental Pembelajaran Mesin* (Hendri Karisma dan Hairul Umam).

| Berkas | Kode/Gambar di buku | Isi |
|---|---|---|
| `knn_manual.py` | Kode 8.1 | kNN dari nol dengan NumPy, suara biasa dan terbobot |
| `knn_scaling.py` | Kode 8.2 | kNN dengan dan tanpa scaling pada data Wine |
| `kurva_k.py` | Gambar kurva error terhadap k | training error dan CV error untuk berbagai k |
| `lwr.py` | Kode 8.3, gambar LWR | locally weighted regression dengan kernel Gaussian; garis lokal pada gambar (h = 0,4) |
| `kutukan_dimensi.py` | Gambar rasio d_min/d_max | simulasi kutukan dimensi |
| `kmeans.py` | Kode 8.4 sampai 8.6, tabel elbow/silhouette | algoritma Lloyd dan k-means++ dari nol, contoh enam titik, elbow dan silhouette dengan scikit-learn |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python knn_manual.py
python knn_scaling.py
python kurva_k.py
python lwr.py
python kutukan_dimensi.py
python kmeans.py
```

Data yang dipakai adalah data bawaan scikit-learn (`load_wine`, `make_moons`, `make_blobs`) atau
dibangkitkan di dalam skrip, sehingga tidak perlu unduhan.
