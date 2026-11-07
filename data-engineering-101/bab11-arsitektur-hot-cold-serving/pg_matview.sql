-- Kode 11.8: materialized view ringkasan nasabah di PostgreSQL (butuh skema gold.fakta_transaksi).
CREATE MATERIALIZED VIEW mv_ringkasan_nasabah AS
SELECT id_nasabah,
       date_trunc('month', tanggal)::date AS bulan,
       count(*)                           AS jumlah_trx,
       sum(nominal)                       AS total_nominal,
       max(tanggal)                       AS trx_terakhir
FROM gold.fakta_transaksi
WHERE tanggal >= date_trunc('month', current_date) - interval '12 months'
GROUP BY id_nasabah, date_trunc('month', tanggal);

-- syarat REFRESH ... CONCURRENTLY: indeks unik pada view
CREATE UNIQUE INDEX ON mv_ringkasan_nasabah (id_nasabah, bulan);

-- dijalankan Airflow setelah gold harian lolos uji
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_ringkasan_nasabah;
