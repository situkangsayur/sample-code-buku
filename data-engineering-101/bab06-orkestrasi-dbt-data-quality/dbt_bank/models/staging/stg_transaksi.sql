-- staging: cast tipe, standarisasi, satu tanggal logis, dedup per trx_id
with sumber as (
    select * from {{ source('bronze', 'transaksi') }}
    where tgl = cast('{{ var("tgl") }}' as date)
)
select
    trx_id,
    rekening_id,
    lower(trim(jenis_akad))                as jenis_akad,
    try_cast(nominal as decimal(18, 2))    as nominal,
    waktu_trx,
    cast(waktu_trx as date)                as tgl,
    _ingest_ts
from sumber
qualify row_number() over (partition by trx_id order by _ingest_ts desc) = 1
