"""Kode 5.4: producer dan consumer Kafka dengan key dan commit manual.

Pemakaian:
  python kafka_pesanan.py kirim 20            # kirim 20 event ber-key
  python kafka_pesanan.py baca notifikasi     # baca sebagai consumer group "notifikasi"
  python kafka_pesanan.py baca analitik       # grup lain membaca topik yang sama
Bootstrap server dari KAFKA (default localhost:9092).
"""
import json, os, sys
from confluent_kafka import Consumer, Producer

BOOT = os.environ.get("KAFKA", "localhost:9092")
TOPIK = "pesanan"


def kirim(n: int) -> None:
    p = Producer({"bootstrap.servers": BOOT,
                  "acks": "all",                # tunggu semua ISR
                  "enable.idempotence": True})  # cegah duplikat akibat retry
    for i in range(n):
        id_pesanan = 1000 + (i % 5)             # 5 key berbeda, urutan per key terjaga
        ev = {"tipe": "PesananDiubah", "id_pesanan": id_pesanan, "urutan": i}
        p.produce(TOPIK, key=str(id_pesanan), value=json.dumps(ev))
    p.flush()
    print(f"terkirim {n} event")


def proses(ev: dict, partisi: int, offset: int) -> None:
    print(f"partisi={partisi} offset={offset} key={ev['id_pesanan']} urutan={ev['urutan']}")


def baca(grup: str) -> None:
    c = Consumer({"bootstrap.servers": BOOT,
                  "group.id": grup,
                  "auto.offset.reset": "earliest",
                  "enable.auto.commit": False})
    c.subscribe([TOPIK])
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None or msg.error():
                continue
            proses(json.loads(msg.value()), msg.partition(), msg.offset())  # harus idempotent
            c.commit(message=msg, asynchronous=False)  # catat offset SETELAH proses
    except KeyboardInterrupt:
        pass
    finally:
        c.close()


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "kirim":
        kirim(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    elif len(sys.argv) >= 2 and sys.argv[1] == "baca":
        baca(sys.argv[2] if len(sys.argv) > 2 else "notifikasi")
    else:
        print(__doc__)
