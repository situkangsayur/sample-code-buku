-- Jumlah baris jam terakhir dibanding jam yang sama pada 4 pekan sebelumnya.
-- {tabel} diganti oleh cek_tabel.py.
WITH per_jam AS (
  SELECT date_trunc('hour', event_time) AS jam, count(*) AS n
  FROM {tabel}
  WHERE event_time >= now() - INTERVAL 29 DAY
  GROUP BY 1
),
kini AS (
  SELECT jam, n FROM per_jam
  WHERE jam = date_trunc('hour', now() - INTERVAL 1 HOUR)
),
riwayat AS (
  SELECT p.n FROM per_jam p, kini k
  WHERE p.jam IN (k.jam - INTERVAL 7 DAY, k.jam - INTERVAL 14 DAY,
                  k.jam - INTERVAL 21 DAY, k.jam - INTERVAL 28 DAY)
)
SELECT (SELECT coalesce(max(n), 0) FROM kini) AS n,
       avg(n) AS mu, stddev_samp(n) AS sigma
FROM riwayat
