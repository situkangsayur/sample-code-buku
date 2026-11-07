-- silver: tabel fakta per transaksi; incremental dengan unique_key
{{ config(materialized='incremental', unique_key='trx_id',
          incremental_strategy='delete+insert') }}
select trx_id, rekening_id as nasabah_id, jenis_akad, nominal, waktu_trx, tgl
from {{ ref('stg_transaksi') }}
{% if is_incremental() %}
  -- batas jendela diturunkan dari tanggal logis, bukan dari max(waktu_trx) tabel ini,
  -- sehingga backfill tanggal lama memproses baris yang sama kapan pun dijalankan.
  -- Mundur satu jam ke hari sebelumnya menangkap baris yang commit terlambat;
  -- unique_key mencegah duplikat.
  where waktu_trx >= cast('{{ var("tgl") }}' as timestamp) - interval 1 hour
    and waktu_trx <  cast('{{ var("tgl") }}' as timestamp) + interval 1 day
{% endif %}
