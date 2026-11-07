"""Pemeriksaan freshness dan volume dengan peringatan webhook.
Dijalankan Airflow tiap 15 menit. Variabel lingkungan:
  TABEL      (bawaan: iceberg_scan('s3://lake/silver/transaksi'))
  WEBHOOK_URL (opsional; dari Vault/secret Airflow). Tanpa itu, pesan dicetak.
Untuk mencoba lokal tanpa Iceberg: python obs/demo_lokal.py
"""
import json
import os
import urllib.request

import duckdb

SLO_MENIT, Z_MAKS = 15, 3.0


def periksa(con, tabel: str) -> list[str]:
    telat = con.sql(f"SELECT date_diff('minute', max(event_time), now()) FROM {tabel}").fetchone()[0]
    q = open(os.path.join(os.path.dirname(__file__), "volume.sql")).read()
    n, mu, sigma = con.sql(q.replace("{tabel}", tabel)).fetchone()
    z = (n - mu) / sigma if sigma else 0.0
    masalah = []
    if telat is None or telat > SLO_MENIT:
        masalah.append(f"freshness: telat {telat} menit")
    if abs(z) > Z_MAKS:
        masalah.append(f"volume: n={n}, z={z:.1f}")
    return masalah


def kirim(masalah: list[str], nama: str) -> None:
    teks = f"[{nama}] " + "; ".join(masalah) + " -- runbook: freshness-silver-transaksi"
    url = os.environ.get("WEBHOOK_URL")
    if not url:
        print(teks)
        return
    req = urllib.request.Request(url, data=json.dumps({"text": teks}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


if __name__ == "__main__":
    con = duckdb.connect()
    tabel = os.environ.get("TABEL", "iceberg_scan('s3://lake/silver/transaksi')")
    if "iceberg_scan" in tabel:
        con.sql("INSTALL iceberg; LOAD iceberg;")   # + kredensial S3 (RustFS/S3) dari env
    m = periksa(con, tabel)
    if m:
        kirim(m, "silver.transaksi")
    else:
        print("OK")
