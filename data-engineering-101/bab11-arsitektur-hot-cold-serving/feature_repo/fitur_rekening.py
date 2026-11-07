"""Kode 11.9: definisi fitur rekening dengan Feast. Jalankan dari folder feature_repo: feast apply"""
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

rekening = Entity(name="rekening", join_keys=["id_rekening"],
                  description="rekening nasabah bank syariah digital")

# offline store: tabel fitur yang ditulis job Spark ke Parquet/Iceberg
sumber_fitur = FileSource(
    name="fitur_rekening_src",
    path="data/fitur_rekening.parquet",
    timestamp_field="event_time",
)

fitur_rekening = FeatureView(
    name="fitur_rekening",
    entities=[rekening],
    ttl=timedelta(days=2),          # nilai lebih tua dari ini dianggap tidak ada
    schema=[
        Field(name="n_trx_10m", dtype=Int64),
        Field(name="n_perangkat_1h", dtype=Int64),
        Field(name="rata_nominal_30h", dtype=Float32),
    ],
    online=True,                    # ikut di-materialize ke online store
    source=sumber_fitur,
)
