"""Kode 5.1: producer RabbitMQ di layanan pesanan.

Pemakaian: python producer_rabbit.py [jumlah]   (default 10 pesan)
Host broker diambil dari AMQP_HOST (default localhost).
"""
import json, os, sys, uuid
import pika

HOST = os.environ.get("AMQP_HOST", "localhost")
ANTREAN = "pesanan.dibuat"


def main(jumlah: int) -> None:
    conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
    ch = conn.channel()
    # durable: queue tetap ada bila broker dijalankan ulang
    ch.queue_declare(queue=ANTREAN, durable=True)
    for i in range(jumlah):
        pesan = {"id_pesanan": 1000 + i, "total": 25000 + i}
        ch.basic_publish(
            exchange="",                       # default exchange: langsung ke queue
            routing_key=ANTREAN,
            body=json.dumps(pesan),
            properties=pika.BasicProperties(
                delivery_mode=2,               # persistent: disimpan ke disk
                message_id=str(uuid.uuid4()),  # dipakai consumer untuk dedup
                content_type="application/json"))
    print(f"terkirim {jumlah} pesan ke {ANTREAN}")
    conn.close()


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
