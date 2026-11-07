-- uji tunggal (singular): total gold harus sama dengan total silver untuk tanggal yang sama
with g as (select tgl, sum(total_nominal) as t from {{ ref('gold_harian_cabang') }} group by tgl),
     s as (select tgl, sum(nominal) as t from {{ ref('fct_transaksi') }} group by tgl)
select g.tgl, g.t as total_gold, s.t as total_silver
from g join s using (tgl)
where abs(g.t - s.t) > 0.01
