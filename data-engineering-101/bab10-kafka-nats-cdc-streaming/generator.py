"""Kode 10.13: generator transaksi dengan pola curiga dan late event.

Menulis langsung ke tabel transaksi di PostgreSQL; Debezium yang meneruskan
setiap INSERT ke topik bank.public.transaksi.

Pemakaian:
    python generator.py                    # skenario buku (pola curiga + 2 late event)
    python generator.py --normal 200       # tambah lalu lintas normal acak
    python generator.py --akad             # contoh outbox pattern (akad + outbox)
"""
import argparse
import json
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

import psycopg

DSN = "postgresql://postgres:rahasia_lab@localhost:5432/bank"
con = psycopg.connect(DSN, autocommit=True)


def tulis(rek, dev, menit_lalu=0):
    # waktu disimpan sebagai TIMESTAMP tanpa zona, dalam UTC
    t = datetime.now(timezone.utc) - timedelta(minutes=menit_lalu)
    con.execute("INSERT INTO transaksi (id_trx, id_rekening, id_perangkat, nominal, waktu)"
                " VALUES (%s, %s, %s, %s, %s)",
                (str(uuid.uuid4()), rek, dev, random.randint(10, 500) * 1000,
                 t.replace(tzinfo=None)))


def skenario_buku():
    for i in range(7):                        # pola curiga: 7 trx, 2 perangkat
        tulis("R-10023", f"HP-{i % 2}")
    tulis("R-10023", "HP-9", menit_lalu=1)    # terlambat, masih diterima
    tulis("R-10023", "HP-9", menit_lalu=5)    # di bawah watermark
    print("skenario buku: 7 transaksi curiga + 2 late event untuk R-10023")


def lalu_lintas_normal(n, jeda):
    """Transaksi wajar: rekening acak, satu perangkat per rekening."""
    for _ in range(n):
        rek = f"R-{random.randint(20000, 20999)}"
        tulis(rek, f"HP-{rek[-3:]}")
        time.sleep(jeda)
    print(f"{n} transaksi normal ditulis")


def akad_dengan_outbox():
    """Outbox pattern: akad dan event-nya dalam SATU transaksi basis data."""
    id_akad = "AK-" + uuid.uuid4().hex[:8].upper()
    payload = {"id_akad": id_akad, "id_nasabah": "N-0042", "jenis": "murabahah",
               "pokok": 120_000_000, "margin": 18_000_000}
    with psycopg.connect(DSN) as c:           # autocommit mati: satu transaksi
        c.execute("INSERT INTO akad (id_akad, id_nasabah, jenis, pokok, margin)"
                  " VALUES (%s, %s, %s, %s, %s)",
                  (id_akad, payload["id_nasabah"], payload["jenis"],
                   payload["pokok"], payload["margin"]))
        c.execute("INSERT INTO outbox (id, aggregatetype, aggregateid, type, payload)"
                  " VALUES (%s, %s, %s, %s, %s)",
                  (uuid.uuid4(), "akad", id_akad, "AkadDibuat", json.dumps(payload)))
        # commit terjadi saat keluar dari blok with; gagal di tengah = keduanya batal
    print(f"akad {id_akad} dan event outbox ditulis (topik pembiayaan.akad)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--normal", type=int, default=0)
    ap.add_argument("--jeda", type=float, default=0.05)
    ap.add_argument("--akad", action="store_true")
    ap.add_argument("--tanpa-skenario", action="store_true")
    a = ap.parse_args()
    if not a.tanpa_skenario:
        skenario_buku()
    if a.normal:
        lalu_lintas_normal(a.normal, a.jeda)
    if a.akad:
        akad_dengan_outbox()


if __name__ == "__main__":
    main()
