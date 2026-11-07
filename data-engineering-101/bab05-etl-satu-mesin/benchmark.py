"""Benchmark agregasi yang sama di pandas, Polars, DuckDB, dan DataFusion.

Tiap engine dijalankan di proses terpisah agar memori puncak (ru_maxrss) adil.
Laporkan median dari minimal tiga kali jalan.
Pemakaian: python benchmark.py [jumlah_ulang]
"""
import json
import statistics
import subprocess
import sys
import time

SRC = "data/bronze/trx/*/*.parquet"
KODE = {
    "pandas": f"""
import pandas as pd, glob
df = pd.concat(pd.read_parquet(f, columns=['kanal','nominal']) for f in glob.glob('{SRC}'))
df['nominal'] = pd.to_numeric(df['nominal'], errors='coerce')
r = df.groupby(df['kanal'].str.upper())['nominal'].sum()""",
    "polars": f"""
import polars as pl
r = (pl.scan_parquet('{SRC}').group_by(pl.col('kanal').str.to_uppercase())
       .agg(pl.col('nominal').cast(pl.Float64, strict=False).sum()).collect())""",
    "duckdb": f"""
import duckdb
r = duckdb.sql("SELECT upper(kanal), sum(TRY_CAST(nominal AS DOUBLE)) FROM '{SRC}' GROUP BY 1").fetchall()""",
    "datafusion": f"""
from datafusion import SessionContext
ctx = SessionContext(); ctx.register_parquet('t', 'data/bronze/trx/')
r = ctx.sql("SELECT upper(kanal), sum(TRY_CAST(nominal AS DOUBLE)) FROM t GROUP BY 1").collect()""",
}
UKUR = """
import resource, time, json
t = time.perf_counter()
{kode}
dt = time.perf_counter() - t
print(json.dumps({{"detik": dt, "maxrss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024}}))
"""


def main(ulang: int) -> None:
    print(f"{'engine':<11}{'median (s)':>12}{'memori puncak (MB)':>20}")
    for nama, kode in KODE.items():
        hasil = []
        for _ in range(ulang):
            out = subprocess.run([sys.executable, "-c", UKUR.format(kode=kode)],
                                 capture_output=True, text=True, check=True).stdout
            hasil.append(json.loads(out.strip().splitlines()[-1]))
        med = statistics.median(h["detik"] for h in hasil)
        mem = max(h["maxrss_mb"] for h in hasil)
        print(f"{nama:<11}{med:>12.3f}{mem:>20.0f}")


if __name__ == "__main__":
    t0 = time.time()
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    print(f"selesai dalam {time.time() - t0:.1f} s")
