{% snapshot nasabah_snapshot %}
{{ config(target_schema='snapshots', unique_key='nasabah_id',
          strategy='timestamp', updated_at='updated_at') }}
select nasabah_id, cabang_id, segmen, updated_at
from {{ source('bronze', 'nasabah') }}
where tgl = cast('{{ var("tgl") }}' as date)
{% endsnapshot %}
