"""Kode 4.12: hidden partitioning dan partition evolution di Iceberg."""
import datetime as dt
import random

import pyarrow as pa
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import BucketTransform, DayTransform
from pyiceberg.types import (DecimalType, LongType, NestedField, StringType,
                             TimestampType)

from katalog import buka_katalog, siapkan_namespace

skema = Schema(
    NestedField(1, "id_trx", StringType(), required=True),
    NestedField(2, "rek_token", StringType(), required=True),
    NestedField(3, "waktu", TimestampType(), required=True),
    NestedField(4, "nominal", DecimalType(18, 2), required=True),
    NestedField(5, "kanal", StringType()),
    identifier_field_ids=[1])
spec = PartitionSpec(PartitionField(source_id=3, field_id=1000,
                                    transform=DayTransform(), name="waktu_day"))


def batch(hari: str, n=3000, seed=1) -> pa.Table:
    r, t0 = random.Random(seed), dt.datetime.fromisoformat(hari)
    return pa.Table.from_pylist([{
        "id_trx": f"{hari}-{i}", "rek_token": f"rk_{r.randint(1, 9999):04x}",
        "waktu": t0 + dt.timedelta(seconds=r.randint(0, 86399)),
        "nominal": r.randint(1, 5000) * 1000, "kanal": "QRIS"} for i in range(n)],
        schema=skema.as_arrow())


cat = buka_katalog()
siapkan_namespace(cat)
if cat.table_exists("silver.trx_partisi"):
    cat.drop_table("silver.trx_partisi")
tbl = cat.create_table("silver.trx_partisi", schema=skema, partition_spec=spec)
for h in ("2026-11-01", "2026-11-02", "2026-11-03"):
    tbl.append(batch(h))

# pengguna cukup memfilter kolom asli; partisi dipangkas otomatis
rencana = list(tbl.scan(row_filter="waktu >= '2026-11-03T00:00:00'").plan_files())
print("berkas total:", len(tbl.inspect.files()), "| dibaca:", len(rencana))

# volume naik: tambah bucket rekening tanpa menulis ulang data lama
with tbl.update_spec() as u:
    u.add_field("rek_token", BucketTransform(16), "rek_bucket")
tbl.append(batch("2026-11-04", n=6000))
ringkas = {}
for f in tbl.inspect.files().to_pylist():
    n, b = ringkas.get(f["spec_id"], (0, 0))
    ringkas[f["spec_id"]] = (n + 1, b + f["record_count"])
for sid, (n, b) in sorted(ringkas.items()):
    print(f"spec {sid}: {n} berkas, {b} baris")
