"""Kode 10.1: producer transaksi dengan acks=all dan idempotence (confluent-kafka).

Versi lengkap: membuat topik bila belum ada, lalu mengirim satu transaksi
contoh (seperti di buku) atau N transaksi acak untuk uji throughput.

Setiap pesan membawa id_perangkat dan event_time karena keduanya dibaca
aturan fraud Flink SQL (flink_fraud.sql, Kode 10.11). event_time ditulis
dalam format "yyyy-MM-dd HH:mm:ss.SSS" (waktu WIB), format bawaan JSON Flink
untuk kolom TIMESTAMP(3).

Pemakaian:
    python producer_transaksi.py                     # satu transaksi T-881
    python producer_transaksi.py --jumlah 100000 --acks 1
"""
import argparse
import json
import random
import time
from datetime import datetime, timedelta, timezone

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

BROKER = "localhost:19092"
TOPIK = "bank.transaksi"
WIB = timezone(timedelta(hours=7))

terkirim = 0
gagal = 0


def laporan(err, msg):
    """Callback dari librdkafka untuk setiap pesan."""
    global terkirim, gagal
    if err is not None:
        gagal += 1
        print("GAGAL:", err)        # di produksi: kirim ke metrik dan alert
    else:
        terkirim += 1


def siapkan_topik(broker, topik, partisi):
    """Membuat topik dengan jumlah partisi tertentu bila belum ada."""
    admin = AdminClient({"bootstrap.servers": broker})
    if topik in admin.list_topics(timeout=10).topics:
        return
    # satu broker di laptop: faktor replikasi 1. Di produksi: 3.
    hasil = admin.create_topics([NewTopic(topik, num_partitions=partisi,
                                          replication_factor=1)])
    for nama, fut in hasil.items():
        try:
            fut.result()
            print(f"topik {nama} dibuat dengan {partisi} partisi")
        except Exception as e:  # topik mungkin dibuat proses lain
            print(f"topik {nama}: {e}")


def buat_producer(broker, acks):
    return Producer({
        "bootstrap.servers": broker,
        "acks": acks,                       # tunggu semua replika ISR bila "all"
        "enable.idempotence": acks == "all",  # cegah duplikat akibat retry
        "linger.ms": 5,                     # kumpulkan pesan 5 ms untuk batch
        "compression.type": "zstd",
    })


def format_event_time(t):
    """Format SQL yang dibaca format JSON Flink: 2026-12-14 12:09:03.000"""
    return t.strftime("%Y-%m-%d %H:%M:%S.") + f"{t.microsecond // 1000:03d}"


def trx_acak(i):
    return {
        "id_trx": f"T-{i:08d}",
        "id_rekening": f"R-{random.randint(10000, 10999)}",
        "id_perangkat": f"HP-{random.randint(0, 3)}",
        "nominal": random.randint(10, 5000) * 1000,
        "kanal": random.choice(["qris", "transfer", "atm", "teller"]),
        "event_time": format_event_time(datetime.now(WIB)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--broker", default=BROKER)
    ap.add_argument("--topik", default=TOPIK)
    ap.add_argument("--partisi", type=int, default=3)
    ap.add_argument("--acks", default="all", choices=["0", "1", "all"])
    ap.add_argument("--jumlah", type=int, default=0,
                    help="0 = kirim satu transaksi contoh saja")
    a = ap.parse_args()

    siapkan_topik(a.broker, a.topik, a.partisi)
    p = buat_producer(a.broker, a.acks)

    if a.jumlah == 0:
        trx = {"id_trx": "T-881", "id_rekening": "R-10023", "id_perangkat": "HP-0",
               "nominal": 250000, "kanal": "qris",
               "event_time": "2026-12-14 12:09:03.000"}   # WIB, format SQL
        # key = id_rekening: semua transaksi satu rekening masuk partisi yang sama
        p.produce(a.topik, key=trx["id_rekening"],
                  value=json.dumps(trx).encode(), on_delivery=laporan)
        p.flush()
        print(f"terkirim={terkirim} gagal={gagal}")
        return

    mulai = time.perf_counter()
    for i in range(a.jumlah):
        trx = trx_acak(i)
        while True:
            try:
                p.produce(a.topik, key=trx["id_rekening"],
                          value=json.dumps(trx).encode(), on_delivery=laporan)
                break
            except BufferError:
                p.poll(0.1)                 # antrean lokal penuh: tunggu sebentar
        p.poll(0)                           # layani callback
    p.flush()
    detik = time.perf_counter() - mulai
    print(f"acks={a.acks} pesan={a.jumlah} terkirim={terkirim} gagal={gagal} "
          f"waktu={detik:.2f}s throughput={a.jumlah / detik:,.0f} pesan/s")


if __name__ == "__main__":
    main()
