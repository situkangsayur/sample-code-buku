"""Kode 4.16 dan Algoritma 4.2: tiga tugas perawatan tabel dengan PyIceberg:
compaction (menulis ulang berkas kecil), expire snapshots, dan mencari
orphan files. Di produksi, gunakan prosedur Spark (spark/rawat_tabel.sql)."""
import datetime as dt
import os
import pathlib
from urllib.parse import urlparse

from data_contoh import bangkit_bronze
from katalog import buka_katalog, siapkan_namespace

cat = buka_katalog()
siapkan_namespace(cat)
if cat.table_exists("bronze.trx_stream"):
    cat.drop_table("bronze.trx_stream")
contoh = bangkit_bronze(200, "2026-11-05", "s-0")
tbl = cat.create_table("bronze.trx_stream", schema=contoh.schema)
for i in range(40):                     # micro-batch: banyak berkas kecil
    tbl.append(bangkit_bronze(200, "2026-11-05", f"s-{i}", mulai_id=i * 1000))
print("sebelum : berkas =", len(tbl.inspect.files()),
      "| snapshot =", len(tbl.snapshots()))

# 1) compaction: baca seluruh isi lalu tulis ulang sebagai berkas besar
semua = tbl.scan().to_arrow()
tbl.overwrite(semua)
print("compact : berkas =", len(tbl.inspect.files()),
      "| baris =", tbl.scan().to_arrow().num_rows)

# 2) expire snapshots: time travel hanya tersedia untuk snapshot tersisa
batas = dt.datetime.now(dt.timezone.utc)
tbl.maintenance.expire_snapshots().older_than(batas).commit()
tbl = cat.load_table("bronze.trx_stream")
print("expire  : snapshot =", len(tbl.snapshots()))

# 3) orphan files: berkas di folder data yang tidak dirujuk metadata
dirujuk = {urlparse(p).path for p in
           tbl.inspect.all_files().column("file_path").to_pylist()}
folder = pathlib.Path(urlparse(tbl.location()).path) / "data"
yatim = [p for p in folder.glob("*.parquet") if str(p) not in dirujuk]
print("orphan  :", len(yatim), "berkas yatim dari", len(list(folder.glob("*.parquet"))))
if os.environ.get("HAPUS_YATIM") == "1":
    for p in yatim:
        p.unlink()
