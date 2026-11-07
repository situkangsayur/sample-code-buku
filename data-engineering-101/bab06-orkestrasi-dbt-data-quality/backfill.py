"""Backfill sederhana tanpa orchestrator: jalankan rentang tanggal secara berurutan,
lalu bandingkan hasil gold sebelum dan sesudah. Selisih harus nol.

  python backfill.py 2026-11-01 2026-11-03
"""
import datetime as dt
import pathlib
import subprocess
import sys

import duckdb

BIN = pathlib.Path(sys.executable).parent
DB = "data/warehouse_dev.duckdb"
SQL = pathlib.Path("checks/idempoten.sql").read_text()


def ringkas() -> list:
    try:
        with duckdb.connect(DB, read_only=True) as c:
            return c.sql(SQL).fetchall()
    except duckdb.Error:
        return []


def jalankan(tgl: str) -> None:
    subprocess.run([sys.executable, "siapkan_bronze.py", tgl], check=True)
    for perintah in ("snapshot", "build"):
        subprocess.run([str(BIN / "dbt"), perintah, "--profiles-dir", ".", "-q",
                        "--vars", f"{{tgl: {tgl}}}"], cwd="dbt_bank", check=True)


if __name__ == "__main__":
    awal, akhir = (dt.date.fromisoformat(x) for x in sys.argv[1:3])
    sebelum = ringkas()
    d = awal
    while d <= akhir:                     # berurutan: SCD-2 butuh urutan waktu
        jalankan(str(d))
        d += dt.timedelta(days=1)
    sesudah = ringkas()
    for a, b in zip(sebelum, sesudah):
        print(a[0], "baris", a[1], "->", b[1], "| total", a[2], "->", b[2],
              "| SAMA" if a == b else "| BEDA")
    if not sebelum:
        print("run pertama:", sesudah)
