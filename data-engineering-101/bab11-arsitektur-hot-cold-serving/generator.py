"""Generator transaksi sintetis ke topik bank.transaksi (langkah 1 latihan).
Jalankan setelah docker compose up: python generator.py --n 5000 --telat 20"""
import argparse, json, random, time, uuid
from datetime import datetime, timedelta, timezone
from confluent_kafka import Producer

CABANG = ["BDG", "JKT", "SBY", "MKS", "PLG"]
JENIS = ["TRANSFER", "QRIS", "TARIK_TUNAI", "BIAYA_ADMIN"]

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=5000)
ap.add_argument("--telat", type=int, default=20, help="jumlah event terlambat 5-15 menit")
ap.add_argument("--bootstrap", default="localhost:19092")
a = ap.parse_args()

p = Producer({"bootstrap.servers": a.bootstrap, "acks": "all", "enable.idempotence": True})
for i in range(a.n + a.telat):
    t = datetime.now(timezone.utc)
    if i >= a.n:                                   # event terlambat di akhir
        t -= timedelta(minutes=random.randint(5, 15))
    rek = f"R-{random.randint(10000, 10999)}"
    e = {"id_trx": str(uuid.uuid4()), "rekening": rek, "cabang": random.choice(CABANG),
         "jenis": random.choices(JENIS, weights=[50, 35, 10, 5])[0],
         "nominal": random.randint(10, 5000) * 1000,
         "event_time": t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}
    p.produce("bank.transaksi", key=rek, value=json.dumps(e))
    if i % 500 == 0:
        p.poll(0)
    time.sleep(0.002)
p.flush()
print(f"terkirim {a.n} event + {a.telat} event terlambat")
