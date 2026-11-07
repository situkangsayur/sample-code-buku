"""Kode 4.14: MERGE koreksi, riwayat, dan time travel pada Delta Lake
dengan delta-rs (paket Python `deltalake`, tanpa JVM)."""
import json
import pathlib
import shutil

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

LOK = "delta/silver_trx"
shutil.rmtree(LOK, ignore_errors=True)

awal = pa.table({"id_trx": ["T-1", "T-2", "T-3"],
                 "nominal": [250_000, 75_000, 1_500_000],
                 "status": ["SUKSES", "SUKSES", "SUKSES"]})
write_deltalake(LOK, awal)                                   # versi 0

koreksi = pa.table({"id_trx": ["T-2", "T-3", "T-4"],
                    "nominal": [75_000, 1_250_000, 40_000],
                    "status": ["BATAL", "SUKSES", "SUKSES"]})
dt = DeltaTable(LOK)
hasil = (dt.merge(source=koreksi, predicate="t.id_trx = k.id_trx",
                  source_alias="k", target_alias="t")
         .when_matched_delete(predicate="k.status = 'BATAL'")
         .when_matched_update_all()
         .when_not_matched_insert_all()
         .execute())                                          # versi 1
print("statistik merge:", {k: hasil[k] for k in
      ("num_target_rows_deleted", "num_target_rows_updated",
       "num_target_rows_inserted")})

print("sekarang:", DeltaTable(LOK).to_pyarrow_table().sort_by("id_trx").to_pylist())
print("versi 0 :", DeltaTable(LOK, version=0).to_pyarrow_table().num_rows, "baris")
for h in DeltaTable(LOK).history():
    print("riwayat :", h["version"], h["operation"])

# isi _delta_log: satu berkas JSON per commit, berisi aksi add/remove
for f in sorted(pathlib.Path(LOK, "_delta_log").glob("*.json")):
    aksi = [list(json.loads(b))[0] for b in f.read_text().splitlines()]
    print(f.name, aksi)
