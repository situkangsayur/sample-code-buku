# Bab 5 - ETL di Satu Mesin: Arrow, Polars, DuckDB, dan DataFusion

Contoh kode lengkap untuk Bab 5 buku *Data Engineering 101*. Studi kasus: transaksi
sintetis bank syariah digital (semua identitas dibangkitkan acak, bukan data nyata).

## Persiapan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python gen_data.py --baris 1_000_000 --hari 7   # membuat data/bronze/...
```

## Daftar contoh

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `gen_data.py` | Pembangkit bronze transaksi dan nasabah, dengan data kotor sengaja | Subbab Praktik Mandiri |
| `buat_sumber.py` | Basis data sumber tiruan (DuckDB) yang meniru `core.transaksi` | Kode 5.2 |
| `incremental_hwm.py` | Incremental load dengan high-water mark dan jendela tumpang tindih | Kode 5.2, Algoritma 5.1 |
| `arrow_buffer.py` | Isi validity bitmap, values, dan offsets buffer Arrow | Kode 5.3 |
| `zero_copy.py` | Berpindah PyArrow -> Polars -> DuckDB -> Arrow | Kode 5.4 |
| `polars_lazy.py` | Eager vs lazy, `explain()`, expression, streaming engine | Kode 5.5, 5.6 |
| `datafusion-rust/` | DataFusion dari Rust (SQL dan DataFrame API) | Kode 5.8 |
| `tiga_engine.py` | Kueri yang sama di Polars, DuckDB, DataFusion; hasil dibandingkan | Kode 5.9 |
| `pipeline.py` | Bronze -> silver -> gold satu tanggal, pseudonymization, pemeriksaan, overwrite partisi | Kode 5.10-5.14, Algoritma 5.2 |
| `benchmark.py` | Median waktu dan memori puncak pandas, Polars, DuckDB, DataFusion (keluarannya membuka bab) | Kode 5.1, 5.15, Tabel 5.9 |

## Menjalankan

```bash
python buat_sumber.py && python incremental_hwm.py run1 && python incremental_hwm.py run2
python arrow_buffer.py
python zero_copy.py
python polars_lazy.py
python tiga_engine.py
TOKEN_SALT=rahasia-lab python pipeline.py 2026-11-02
TOKEN_SALT=rahasia-lab python pipeline.py 2026-11-02   # dijalankan ulang: hasil identik
python benchmark.py 3

# Rust (butuh toolchain Rust stabil); jalankan dari folder ini
cargo run --release --manifest-path datafusion-rust/Cargo.toml
```

Kode `incremental_hwm.py` memakai berkas DuckDB sebagai sumber agar dapat dijalankan
tanpa server. Untuk PostgreSQL, ganti baris `ATTACH` sesuai komentar di berkas itu.

Versi yang diuji tercantum di `requirements.txt` dan `datafusion-rust/Cargo.toml`.
API Polars dan DataFusion bergerak cepat; cocokkan dengan dokumentasi versi Anda.
