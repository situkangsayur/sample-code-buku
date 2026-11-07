"""Pembangkit data bronze sintetis untuk Bab 4 (bank syariah digital).

Semua identitas dibangkitkan acak; tidak ada data nasabah sungguhan.
Data sengaja dibuat kotor: nominal sebagai teks (kadang rusak), kanal
dengan huruf besar-kecil campur, dan duplikat dari jendela ingest yang
tumpang tindih. Inilah bentuk khas tabel bronze.
"""
from __future__ import annotations

import datetime as dt
import random

import pyarrow as pa

KANAL = ["QRIS", "qris", "MOBILE", "Mobile", "ATM", "AGEN", "TELLER"]
CABANG = ["BGR01", "BGR02", "JKT01", "JKT02", "BDG01", "SBY01"]

SKEMA_BRONZE = pa.schema([
    ("id_trx", pa.string()),
    ("rek", pa.string()),
    ("nik", pa.string()),
    ("nominal", pa.string()),      # teks, persis seperti sumber
    ("kanal", pa.string()),
    ("cabang", pa.string()),
    ("status", pa.string()),
    ("waktu", pa.string()),
    ("_ingest_ts", pa.timestamp("us")),
    ("_source", pa.string()),
    ("_batch_id", pa.string()),
])


def bangkit_bronze(n: int, tanggal: str, batch_id: str, seed: int = 7,
                   mulai_id: int = 1) -> pa.Table:
    """Kembalikan n baris bronze untuk satu tanggal (plus sekitar 2% duplikat)."""
    rng = random.Random(f"{seed}-{tanggal}-{batch_id}")
    hari = dt.datetime.fromisoformat(tanggal)
    ingest = hari + dt.timedelta(days=1, hours=1)
    baris = []
    for i in range(n):
        nominal = str(rng.choice([25_000, 50_000, 100_000, 250_000, 1_500_000])
                      + rng.randint(0, 999))
        if rng.random() < 0.005:
            nominal = nominal[:-1] + "a"          # nilai rusak dari sumber
        waktu = hari + dt.timedelta(seconds=rng.randint(0, 86_399))
        baris.append({
            "id_trx": f"T-{mulai_id + i:08d}",
            "rek": f"{rng.randint(1, 50_000):07d}",
            "nik": f"3201{rng.randint(0, 10**12 - 1):012d}",
            "nominal": nominal,
            "kanal": rng.choice(KANAL),
            "cabang": rng.choice(CABANG),
            "status": "BATAL" if rng.random() < 0.01 else "SUKSES",
            "waktu": waktu.strftime("%Y-%m-%d %H:%M:%S"),
            "_ingest_ts": ingest,
            "_source": "core.transaksi",
            "_batch_id": batch_id,
        })
    # duplikat: baris yang sama terambil dua kali, ingest beberapa menit kemudian
    for b in rng.sample(baris, k=max(1, n // 50)):
        d = dict(b)
        d["_ingest_ts"] = ingest + dt.timedelta(minutes=5)
        baris.append(d)
    return pa.Table.from_pylist(baris, schema=SKEMA_BRONZE)


if __name__ == "__main__":
    t = bangkit_bronze(10, "2026-11-02", "b-20261103")
    import polars as pl
    print(pl.from_arrow(t))
