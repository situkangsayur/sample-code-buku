"""Pipeline yang sama dalam gaya Dagster: berpikir per asset dan per partisi harian.

Jalankan UI:   dagster dev -m dagster_bank.definitions   (dari folder bab06)
Tanpa UI:      python -m dagster_bank.definitions 2026-10-05
"""
import pathlib
import subprocess
import sys

import duckdb
from dagster import (AssetCheckResult, AssetExecutionContext, DailyPartitionsDefinition,
                     Definitions, asset, asset_check, materialize)

PROYEK = pathlib.Path(__file__).resolve().parents[1]
BIN = pathlib.Path(sys.executable).parent
harian = DailyPartitionsDefinition(start_date="2026-01-01", timezone="Asia/Jakarta")


def dbt(*args: str, tgl: str) -> None:
    subprocess.run([str(BIN / "dbt"), *args, "--profiles-dir", ".",
                    "--vars", f"{{tgl: {tgl}}}"], cwd=PROYEK / "dbt_bank", check=True)


@asset(partitions_def=harian, group_name="bronze")
def bronze_transaksi(context: AssetExecutionContext) -> None:
    """Partisi bronze untuk satu tanggal, ditimpa utuh."""
    subprocess.run([sys.executable, "siapkan_bronze.py", context.partition_key],
                   cwd=PROYEK, check=True)


@asset(partitions_def=harian, deps=[bronze_transaksi], group_name="silver")
def silver_transaksi(context: AssetExecutionContext) -> None:
    dbt("snapshot", tgl=context.partition_key)
    dbt("build", "--select", "+fct_transaksi", tgl=context.partition_key)


@asset(partitions_def=harian, deps=[silver_transaksi], group_name="gold")
def gold_harian_cabang(context: AssetExecutionContext) -> None:
    dbt("build", "--select", "gold_harian_cabang+", tgl=context.partition_key)


@asset_check(asset=gold_harian_cabang)
def gold_tidak_kosong() -> AssetCheckResult:
    con = duckdb.connect(str(PROYEK / "data/warehouse_dev.duckdb"), read_only=True)
    n = con.sql("select count(*) from gold_harian_cabang").fetchone()[0]
    return AssetCheckResult(passed=n > 0, metadata={"baris": n})


defs = Definitions(assets=[bronze_transaksi, silver_transaksi, gold_harian_cabang],
                   asset_checks=[gold_tidak_kosong])

if __name__ == "__main__":
    tgl = sys.argv[1] if len(sys.argv) > 1 else "2026-10-05"
    hasil = materialize([bronze_transaksi, silver_transaksi, gold_harian_cabang],
                        partition_key=tgl)
    print("sukses:", hasil.success)
