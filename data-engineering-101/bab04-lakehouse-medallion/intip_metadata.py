"""Kode 4.5: menelusuri pohon metadata Iceberg dari atas ke bawah:
metadata.json -> manifest list -> manifest -> berkas data + statistik.
Jalankan iceberg_dasar.py lebih dulu."""
import json
from urllib.parse import urlparse

from katalog import buka_katalog

tbl = buka_katalog().load_table("bronze.trx")
io = tbl.io

# 1) metadata.json: berkas JSON biasa
meta = json.loads(io.new_input(tbl.metadata_location).open().read())
print("format-version   :", meta["format-version"])
print("current-snapshot :", meta["current-snapshot-id"])
print("jumlah snapshot  :", len(meta["snapshots"]))
print("jumlah skema     :", len(meta["schemas"]))

# 2) manifest list milik snapshot aktif
snap = tbl.current_snapshot()
print("manifest list    :", urlparse(snap.manifest_list).path.split("/")[-1])

# 3) manifest dan 4) berkas data beserta statistik kolom
for m in snap.manifests(io):
    print("  manifest:", m.manifest_path.split("/")[-1],
          "| berkas ditambah:", m.added_files_count)
    for e in m.fetch_manifest_entry(io, discard_deleted=True):
        f = e.data_file
        print("    data:", f.file_path.split("/")[-1],
              "| baris:", f.record_count,
              "| byte:", f.file_size_in_bytes)

# statistik min/maks per kolom yang dipakai untuk melewati berkas
files = tbl.inspect.files().to_pylist()
for f in files:
    m = f["readable_metrics"]["id_trx"]
    print("  id_trx min..maks:", m["lower_bound"], "..", m["upper_bound"])
