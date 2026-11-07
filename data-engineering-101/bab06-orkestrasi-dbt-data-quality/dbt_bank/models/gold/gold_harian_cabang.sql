-- gold: agregat harian per cabang dan akad; satu run menimpa partisi tgl dan tgl-1
-- (tgl-1 ikut dihitung ulang karena baris terlambat dari jam terakhir kemarin
--  bisa baru masuk fct_transaksi pada run hari ini)
{{ config(materialized='incremental', unique_key='tgl',
          incremental_strategy='delete+insert') }}
select f.tgl, d.cabang_id, f.jenis_akad,
       count(*)       as jml_trx,
       sum(f.nominal) as total_nominal
from {{ ref('fct_transaksi') }} f
join {{ ref('dim_nasabah') }} d
  on f.nasabah_id = d.nasabah_id
 and f.waktu_trx >= d.berlaku_dari and f.waktu_trx < d.berlaku_sampai
where f.tgl between cast('{{ var("tgl") }}' as date) - 1
                and cast('{{ var("tgl") }}' as date)
group by all
