-- models/gold/kpi_aktivasi_harian.sql (dialek DuckDB)
with baru as (
  select nasabah_id, tgl_buka
  from {{ ref('dim_nasabah') }}
  where tgl_buka <= current_date - interval 30 day  -- sudah bisa dinilai
),
trx as (
  select nasabah_id, min(tgl_trx) as trx_pertama
  from {{ ref('fct_transaksi') }}
  where jenis = 'FINANSIAL' and dibuat_oleh = 'NASABAH'
  group by nasabah_id
)
select b.tgl_buka,
       count(*) as nasabah_baru,
       sum(case when t.trx_pertama <= b.tgl_buka + interval 30 day
                then 1 else 0 end) as aktif_30h
from baru b left join trx t using (nasabah_id)
group by b.tgl_buka
