-- Kode 11.2: kueri gabungan Lambda. Coba dengan: python lambda_demo.py
-- batas_batch: satu baris berisi waktu terakhir yang tercakup batch
WITH tb AS (
  SELECT max(tercakup_sampai) AS t FROM batch_meta
),
gabung AS (
  SELECT b.cabang, b.jumlah, b.total
  FROM batch_view_cabang_jam b, tb
  WHERE b.jam >= DATE '2026-10-20' AND b.jam < tb.t
  UNION ALL
  SELECT r.cabang, r.jumlah, r.total
  FROM realtime_view_cabang_menit r, tb
  WHERE r.menit >= tb.t                       -- hanya celah sejak batch
)
SELECT cabang,
       sum(jumlah) AS jumlah_trx,
       sum(total)  AS total_nominal
FROM gabung
GROUP BY cabang
ORDER BY cabang;
