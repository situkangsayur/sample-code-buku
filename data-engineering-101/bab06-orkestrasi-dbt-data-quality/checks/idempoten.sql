-- Bukti idempotency: jalankan sebelum dan sesudah backfill, hasilnya harus identik
select tgl,
       sum(jml_trx)       as baris,
       sum(total_nominal) as total
from gold_harian_cabang
where tgl between date '2026-11-01' and date '2026-11-03'
group by tgl
order by tgl;
