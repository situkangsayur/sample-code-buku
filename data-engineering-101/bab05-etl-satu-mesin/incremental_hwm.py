"""Incremental load dengan high-water mark dan jendela tumpang tindih.

Sumber default: data/core.duckdb (buat dulu dengan buat_sumber.py).
Untuk PostgreSQL, ganti ATTACH dengan:
  INSTALL postgres; LOAD postgres;
  ATTACH 'dbname=core host=localhost user=etl' AS core (TYPE postgres, READ_ONLY);
dan kredensial diambil dari secret manager, bukan ditulis di kode.
"""
import json
import pathlib
import sys
import uuid

import duckdb

STATE = pathlib.Path("state/trx_hwm.json")
OVERLAP = "1 hour"                        # jendela tumpang tindih


def main(run_id: str) -> None:
    hwm = json.loads(STATE.read_text())["hwm"] if STATE.exists() else "1970-01-01"
    con = duckdb.connect()
    con.sql("ATTACH 'data/core.duckdb' AS core (READ_ONLY)")
    batch = con.execute(f"""
        SELECT *, now() AS _ingest_ts, 'core.transaksi' AS _source,
               ? AS _batch_id
        FROM core.transaksi
        WHERE updated_at > CAST(? AS TIMESTAMP) - INTERVAL '{OVERLAP}'
    """, [run_id, hwm]).pl()             # parameter, bukan f-string untuk nilai
    if batch.height == 0:
        print("tidak ada data baru"); return
    out = pathlib.Path(f"data/bronze_inc/trx/batch={run_id}")
    out.mkdir(parents=True, exist_ok=True)
    batch.write_parquet(out / "part-0.parquet")
    baru = batch["updated_at"].max()
    # HWM disimpan SETELAH batch berhasil ditulis
    STATE.parent.mkdir(exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"hwm": str(baru)}))
    tmp.replace(STATE)                    # rename atomik
    print(f"run {run_id}: {batch.height} baris, hwm baru {baru}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else uuid.uuid4().hex[:8])
