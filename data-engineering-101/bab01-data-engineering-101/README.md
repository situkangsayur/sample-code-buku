# Bab 1 - Data Engineering 101

Kode lengkap untuk Bab 1 buku *Data Engineering 101*. Semua data bersifat sintetis.

## Persiapan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Daftar contoh

| Berkas | Kode di buku | Isi |
|---|---|---|
| `bangkit_data.py` | (pendukung) | Pembangkit transaksi sintetis bank syariah digital |
| `alur_mini.py` | Kode 1.1 | Lima tahap lifecycle: generation, ingestion, storage, transformation, serving |
| `hitung_skala.py` | Kode 1.2 | Hitungan kasar waktu baca 1 TB dan volume transaksi |
| `pilih_tier.py` | Kode 1.3 | Aturan sederhana memilih tier hot/warm/cold/archive |
| `tiga-bahasa/total_kanal.py` | Kode 1.4 | Total per kanal dengan Polars (Python) |
| `tiga-bahasa/scala/` | Kode 1.5 | Total per kanal dengan Spark (Scala, sbt) |
| `tiga-bahasa/rust/` | Kode 1.6 | Total per kanal dengan DataFusion (Rust, cargo) |

## Cara menjalankan

```bash
python hitung_skala.py
python pilih_tier.py
python alur_mini.py              # menghasilkan folder lake/bronze, lake/silver, lake/gold

cd tiga-bahasa
python total_kanal.py            # membaca ../lake/silver/transaksi.parquet
(cd rust && cargo run --release)  # kompilasi pertama memakan beberapa menit
(cd scala && sbt run)             # butuh JDK 17 atau 21 dan sbt
```

Jalankan `alur_mini.py` lebih dulu karena contoh tiga bahasa membaca berkas silver yang dihasilkannya.
