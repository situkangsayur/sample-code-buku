"""Kode 4.19-4.22: pipeline medallion bronze -> silver -> gold di atas Iceberg.

Pemakaian:  TOKEN_SALT=rahasia-lab python medallion.py 2026-11-02
Dijalankan berkali-kali untuk tanggal yang sama, hasilnya identik (idempotent):
bronze menolak batch yang sudah ada, silver dan gold menimpa partisi tanggalnya.
"""
import datetime as dt
import hashlib
import hmac
import os
import sys
import warnings

import duckdb
import polars as pl
from pyiceberg.transforms import DayTransform, IdentityTransform

from data_contoh import bangkit_bronze
from katalog import buka_katalog, siapkan_namespace

warnings.filterwarnings("ignore", message="Delete operation did not match")
cat = buka_katalog()
siapkan_namespace(cat)
# bronze.trx sisa demo iceberg_dasar.py (kolom rek sudah diganti nama) tidak dipakai
if cat.table_exists("bronze.trx") and "rek" not in [
        f.name for f in cat.load_table("bronze.trx").schema().fields]:
    cat.drop_table("bronze.trx")


def tabel(nama, contoh, kolom_partisi=None, transform=None):
    """Buat tabel bila belum ada (skema dari contoh data), lalu muat."""
    if not cat.table_exists(nama):
        t = cat.create_table(nama, schema=contoh.schema)
        if kolom_partisi:
            with t.update_spec() as u:
                u.add_field(kolom_partisi, transform, f"{kolom_partisi}_part")
    return cat.load_table(nama)


# ---------------------------------------------------------------- bronze
def ke_bronze(tgl: str) -> str:
    batch_id = "b-" + tgl.replace("-", "")
    raw = bangkit_bronze(20_000, tgl, batch_id,
                         mulai_id=int(tgl[-2:]) * 1_000_000)
    br = tabel("bronze.trx", raw)
    sudah = br.scan(row_filter=f"_batch_id == '{batch_id}'",
                    selected_fields=("id_trx",)).to_arrow().num_rows
    if sudah == 0:                          # append-only, sekali per batch
        br.append(raw)
    return batch_id


# ---------------------------------------------------------------- silver
def ke_silver(batch_id: str, tgl: str):
    kunci = os.environ.get("TOKEN_SALT", "rahasia-lab").encode()
    token = lambda r: hmac.new(kunci, r.encode(), hashlib.sha256).hexdigest()[:20]
    raw = pl.from_arrow(cat.load_table("bronze.trx").scan(
        row_filter=f"_batch_id == '{batch_id}'").to_arrow())
    rapi = (raw
        .with_columns(
            pl.col("nominal").cast(pl.Int64, strict=False).alias("nominal_num"),
            pl.col("waktu").str.to_datetime("%Y-%m-%d %H:%M:%S").dt.cast_time_unit("us"),
            pl.col("kanal").str.to_uppercase())
        .sort("_ingest_ts", descending=True)
        .unique(subset="id_trx", keep="first", maintain_order=True))
    buruk = rapi.filter(pl.col("nominal_num").is_null() | (pl.col("nominal_num") <= 0))
    baik = (rapi.filter(pl.col("nominal_num") > 0)
        .with_columns(
            pl.col("rek").map_elements(token, return_dtype=pl.String)
              .alias("rek_token"))                  # pseudonim; NIK dibuang
        .select("id_trx", "rek_token", "cabang", "kanal", "status", "waktu",
                pl.col("nominal_num").alias("nominal"), "_batch_id"))
    gerbang_silver(baik)                            # gagal -> berhenti
    if buruk.height:
        k = (buruk.select("id_trx", "nominal", "_batch_id")
             .with_columns(pl.lit("nominal tidak valid").alias("alasan")).to_arrow())
        kt = tabel("silver.trx_karantina", k)
        kt.overwrite(k, overwrite_filter=f"_batch_id == '{batch_id}'")
    besok = (dt.date.fromisoformat(tgl) + dt.timedelta(days=1)).isoformat()
    arr = baik.to_arrow()
    si = tabel("silver.trx", arr, "waktu", DayTransform())
    si.overwrite(arr, overwrite_filter=(f"waktu >= '{tgl}T00:00:00' and "
                                        f"waktu < '{besok}T00:00:00'"))
    return baik.height, buruk.height


def gerbang_silver(df: pl.DataFrame):
    """Gerbang data quality bronze -> silver (versi ringkas)."""
    cek = {
        "id_trx unik": df["id_trx"].n_unique() == df.height,
        "tanpa null": df.null_count().sum_horizontal().item() == 0,
        "nominal > 0": bool((df["nominal"] > 0).all()),
        "kolom nik hilang": "nik" not in df.columns,
    }
    gagal = [k for k, ok in cek.items() if not ok]
    if gagal:
        raise ValueError(f"gerbang silver gagal: {gagal}")


# ------------------------------------------------------------------ gold
def ke_gold(tgl: str):
    besok = (dt.date.fromisoformat(tgl) + dt.timedelta(days=1)).isoformat()
    silver = cat.load_table("silver.trx").scan(row_filter=(
        f"waktu >= '{tgl}T00:00:00' and waktu < '{besok}T00:00:00'")).to_arrow()
    gold = duckdb.sql("""
        SELECT CAST(waktu AS DATE) AS tanggal, cabang, kanal,
               COUNT(*) AS jml_trx, SUM(nominal) AS total
        FROM silver WHERE status = 'SUKSES'
        GROUP BY ALL ORDER BY ALL""").arrow()
    if hasattr(gold, "read_all"):               # DuckDB baru: RecordBatchReader
        gold = gold.read_all()
    go = tabel("gold.trx_harian_cabang", gold, "tanggal", IdentityTransform())
    go.overwrite(gold, overwrite_filter=f"tanggal == '{tgl}'")
    return gold.num_rows


if __name__ == "__main__":
    tgl = sys.argv[1] if len(sys.argv) > 1 else "2026-11-02"
    bid = ke_bronze(tgl)
    n_baik, n_buruk = ke_silver(bid, tgl)
    n_gold = ke_gold(tgl)
    for nama in ("bronze.trx", "silver.trx", "gold.trx_harian_cabang"):
        t = cat.load_table(nama)
        print(f"{nama:24s} baris={t.scan().to_arrow().num_rows:7d} "
              f"snapshot={len(t.snapshots())}")
    print(f"silver baik={n_baik} karantina={n_buruk} | gold baris={n_gold}")
