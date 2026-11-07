-- dimensi SCD tipe 2 dari snapshot: satu baris per versi profil nasabah
select nasabah_id, cabang_id, segmen,
       dbt_valid_from as berlaku_dari,
       coalesce(dbt_valid_to, timestamp '9999-12-31') as berlaku_sampai,
       dbt_valid_to is null as versi_terkini
from {{ ref('nasabah_snapshot') }}
