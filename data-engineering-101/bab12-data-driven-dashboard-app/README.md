# Bab 12 - Data-driven: dari metrik ke dashboard dan data app

Contoh kode untuk Bab 12 buku *Data Engineering 101* (studi kasus bank syariah digital,
semua data sintetis).

| Berkas | Isi | Kode di buku |
|---|---|---|
| `dbt/models/semantic/nasabah.yml` | model semantik dan metrik rasio aktivasi | Kode 12.1 |
| `dbt/models/gold/kpi_aktivasi_harian.sql` | model dbt KPI aktivasi harian | Kode 12.2 |
| `pit_asof_join.py` | as-of join DuckDB (point-in-time) vs join salah | Kode 12.3 |
| `ab_test.py` | ukuran sampel, SRM, uji dua proporsi, simulasi peeking | Kode 12.4 |
| `spark_gold_ke_postgres.py` | memuat agregat gold ke PostgreSQL (JDBC, idempotent) | Kode 12.5 |
| `docker-compose.yml`, `sql/init.sh` | PostgreSQL serving + Metabase (versi dikunci), akun read-only dengan password dari .env | Kode 12.6 |
| `gen_gold.py` | membangkitkan `gold.duckdb` sintetis | - |
| `app_streamlit.py` | data app KPI cabang + form pelabelan fraud | Kode 12.7, 12.8 |
| `api_fastapi.py` | API KPI dengan pemeriksaan akses per cabang | Kode 12.9 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python gen_gold.py                 # membuat gold.duckdb
python pit_asof_join.py
python ab_test.py
streamlit run app_streamlit.py     # http://localhost:8501
uvicorn api_fastapi:app --reload   # http://localhost:8000/docs
cp .env.example .env && docker compose up -d   # Metabase di http://localhost:3000
```

`spark_gold_ke_postgres.py` membutuhkan klaster Spark dengan katalog Iceberg `lake`
(lihat contoh Bab 9 dan Bab 11). Model dbt dijalankan di dalam proyek dbt dari Bab 6.
Nomor Kode mengikuti urutan di bab; periksa kembali bila bab disunting.
