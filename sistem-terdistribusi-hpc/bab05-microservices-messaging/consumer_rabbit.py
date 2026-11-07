"""Kode 5.2: consumer RabbitMQ di layanan notifikasi.

Ack dikirim SETELAH pekerjaan selesai (at-least-once).
Variabel JEDA_SEBELUM_ACK (detik) dipakai untuk eksperimen "mati sebelum ack".
"""
import json, os, time
import pika

HOST = os.environ.get("AMQP_HOST", "localhost")
ANTREAN = "pesanan.dibuat"
JEDA = float(os.environ.get("JEDA_SEBELUM_ACK", "0"))


class FormatRusak(Exception):
    pass


def kirim_notifikasi(id_pesan, pesanan):
    if "id_pesanan" not in pesanan:
        raise FormatRusak(id_pesan)
    print(f"[notif] pesanan {pesanan['id_pesanan']} (pesan {id_pesan})", flush=True)


def tangani(ch, method, props, body):
    try:
        pesanan = json.loads(body)
        kirim_notifikasi(props.message_id, pesanan)   # harus idempotent
        time.sleep(JEDA)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except (FormatRusak, json.JSONDecodeError):
        # jangan diulang: buang (atau ke dead letter queue bila dikonfigurasi)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    for _ in range(30):                       # tunggu broker siap
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(1)
    ch = conn.channel()
    ch.queue_declare(queue=ANTREAN, durable=True)
    ch.basic_qos(prefetch_count=10)           # maksimal 10 pesan belum di-ack
    ch.basic_consume(queue=ANTREAN, on_message_callback=tangani)
    print("menunggu pesan...", flush=True)
    ch.start_consuming()


if __name__ == "__main__":
    main()
