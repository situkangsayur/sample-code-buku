# Bab 2 - Pemodelan Data dan Format Penyimpanan

Kode lengkap untuk Bab 2 buku *Data Engineering 101*. Semua data bersifat sintetis.

## Persiapan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Daftar contoh

| Berkas | Kode di buku | Isi |
|---|---|---|
| `bangkit_data.py` | (pendukung) | Pembangkit transaksi sintetis |
| `olap_kubus.py` | Kode 2.1 | Roll-up, CUBE, slice, dice, pivot dengan SQL DuckDB |
| `star_schema.sql` | Kode 2.2 | DDL star schema, data contoh, kueri kota saat kejadian vs sekarang |
| `scd2.py` | Kode 2.3 | SCD tipe 1 dan tipe 2 pada `dim_nasabah` |
| `urutkan_dan_pangkas.py` | Kode 2.4 | Pengaruh urutan data terhadap predicate pushdown |
| `intip_parquet.py` | Kode 2.5 | Membaca metadata Parquet dengan PyArrow |
| `rust/` | Kode 2.6 | Membaca metadata Parquet dengan crate `parquet` |
| `ukur_format.py` | Kode 2.7 | Ukuran berkas dan waktu kueri CSV, JSON Lines, Parquet |
| (di buku saja) | Kode 2.8 | Contoh skema Avro versi 1 dan 2 |
| `evolusi_skema.py` | Kode 2.9 | Membaca dua versi skema Parquet dengan `union_by_name` |

## Cara menjalankan

```bash
python olap_kubus.py
python scd2.py
duckdb < star_schema.sql            # atau jalankan per pernyataan dari Python
python ukur_format.py --baris 2000000 --ulang 5   # menghasilkan data/trx.*
python intip_parquet.py             # membaca data/trx.parquet
python urutkan_dan_pangkas.py
python evolusi_skema.py
(cd rust && cargo run --release -- ../data/trx.parquet)
```

Angka waktu sangat bergantung pada mesin. Laporkan median beberapa kali jalan, bukan sekali jalan.
