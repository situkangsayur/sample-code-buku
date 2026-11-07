"""Kode 4.3, 4.4, dan 4.10: tabel Iceberg pertama, snapshot, time travel,
schema evolution, dan rollback dengan PyIceberg (tanpa JVM)."""
from pyiceberg.types import StringType

from data_contoh import bangkit_bronze
from katalog import buka_katalog, siapkan_namespace

cat = buka_katalog()
siapkan_namespace(cat)
if cat.table_exists("bronze.trx"):
    cat.drop_table("bronze.trx")

hari1 = bangkit_bronze(5_000, "2026-11-01", "b-20261102")
tbl = cat.create_table("bronze.trx", schema=hari1.schema)
tbl.append(hari1)                                   # snapshot 1
tbl.append(bangkit_bronze(5_000, "2026-11-02", "b-20261103",
                          mulai_id=5_001))          # snapshot 2

print("metadata terbaru:", tbl.metadata_location)
for s in tbl.snapshots():                           # riwayat snapshot
    print(s.snapshot_id, s.timestamp_ms, s.summary.operation.value,
          s.summary.get("added-records"))

sid1 = tbl.snapshots()[0].snapshot_id
print("baris sekarang :", tbl.scan().to_arrow().num_rows)
print("baris snapshot1:", tbl.scan(snapshot_id=sid1).to_arrow().num_rows)

with tbl.update_schema() as u:                      # schema evolution
    u.add_column("perangkat", StringType(), doc="jenis perangkat nasabah")
    u.rename_column("rek", "no_rekening")
print("kolom:", [f.name for f in tbl.schema().fields])
print("berkas data tetap:", len(tbl.inspect.files()))

# job rusak menghapus semua transaksi QRIS, lalu dibatalkan
tbl.delete(delete_filter="kanal == 'QRIS'")
print("setelah delete :", tbl.scan().to_arrow().num_rows)
tbl.manage_snapshots().rollback_to_snapshot(tbl.snapshots()[-2].snapshot_id).commit()
print("setelah rollback:", tbl.scan().to_arrow().num_rows)
