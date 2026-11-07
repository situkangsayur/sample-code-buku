# Bab 6 - Orchestration, dbt, dan Data Quality

Contoh kode lengkap untuk Bab 6 buku *Data Engineering 101*. Pipeline harian bank syariah
digital (data sintetis): bronze Parquet -> dbt-duckdb (staging, silver, gold) dengan
data quality test, dijadwalkan oleh Airflow 3 atau Dagster.

## Persiapan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Airflow sebaiknya dipasang di virtualenv terpisah dengan constraints resmi, misalnya
`pip install "apache-airflow==3.x.y" --constraint <URL constraints resmi>`.
Contoh diuji dengan Airflow 3.3.2, dbt-core 1.12.5 + dbt-duckdb 1.11.0, Dagster 1.13.26.

## Daftar contoh

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `siapkan_bronze.py` | Bronze sintetis per tanggal; opsi `--sabotase` (50 trx_id ganda + 1 akad tidak valid) | Praktik mandiri |
| `dags/trx_harian.py` | DAG harian Airflow 3 (TaskFlow, catchup, retry) | Kode 6.1 |
| `dagster_bank/definitions.py` | Asset berpartisi harian dan asset check di Dagster | Kode 6.2 |
| `backfill.py`, `checks/idempoten.sql` | Backfill rentang tanggal dan bukti idempotency | Kode 6.3, Contoh backfill |
| `dbt_bank/models/staging/stg_transaksi.sql` | Model staging | Kode 6.4 |
| `dbt_bank/models/silver/fct_transaksi.sql` | Model incremental | Kode 6.5 |
| `dbt_bank/snapshots/nasabah_snapshot.sql`, `models/silver/dim_nasabah.sql` | Snapshot SCD tipe 2 | Kode 6.6 |
| `dbt_bank/models/gold/gold_harian_cabang.sql` | Gold: overwrite partisi tgl dan tgl-1 (delete+insert) | Subbab dbt |
| `dbt_bank/models/schema.yml`, `macros/tests.sql`, `sources.yml` | Uji generik, uji buatan sendiri, freshness | Kode 6.7 |
| `dbt_bank/tests/rekonsiliasi_gold_silver.sql` | Uji tunggal rekonsiliasi | Kode 6.8 |
| `soda/checks.yml` | Pemeriksaan SodaCL (perlu paket soda-core-duckdb) | Kode 6.9 |
| `kontrak/transaksi.yaml` | Contoh data contract | Kode 6.10 |
| `.github/workflows/dbt-ci.yml` | CI dbt per pull request | Kode 6.11 |
| `docker-compose.yml` | Stack lab (PostgreSQL + Airflow standalone) | Praktik mandiri |

## Menjalankan

```bash
# 1) backfill 1-3 November, lalu ulangi: semua baris harus "SAMA"
python backfill.py 2026-11-01 2026-11-03
python backfill.py 2026-11-01 2026-11-03

# 2) sabotase: uji accepted_values gagal, fct_transaksi dan gold di-SKIP
python siapkan_bronze.py 2026-11-04 --sabotase
cd dbt_bank
dbt snapshot --profiles-dir . --vars '{tgl: 2026-11-04}'
dbt build    --profiles-dir . --vars '{tgl: 2026-11-04}'
cd ..

# 3) Airflow (virtualenv Airflow): uji satu tanggal tanpa scheduler
export AIRFLOW__CORE__DAGS_FOLDER=$PWD/dags PROYEK_DIR=$PWD PY_BIN=$(dirname $(which dbt))
airflow db migrate && airflow dags test trx_harian 2026-11-05

# 4) Dagster
python -m dagster_bank.definitions 2026-10-05      # tanpa UI
dagster dev -m dagster_bank.definitions            # dengan UI
```

Catatan: Dagster hanya mengenal partisi sampai waktu sekarang, sehingga tanggal di masa
depan baru dapat dimaterialisasi setelah tanggalnya tiba.
