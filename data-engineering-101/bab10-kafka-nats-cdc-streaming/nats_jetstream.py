"""Kode 10.6: NATS JetStream, publish dengan deduplikasi dan pull consumer (nats-py).

Versi lengkap: dibandingkan juga dengan NATS core (tanpa persistensi),
supaya terlihat bahwa pesan core hilang bila tidak ada pelanggan saat itu.

Pemakaian:
    python nats_jetstream.py
"""
import asyncio

import nats
from nats.errors import TimeoutError as NatsTimeout
from nats.js.errors import BadRequestError

URL = "nats://localhost:4222"


async def demo_core(nc):
    """NATS core: pub-sub tanpa penyimpanan, at-most-once."""
    await nc.publish("info.kurs", b"USD=16000")      # belum ada pelanggan: hilang
    diterima = []

    async def cb(m):
        diterima.append(m.data)

    sub = await nc.subscribe("info.kurs", cb=cb)
    await nc.publish("info.kurs", b"USD=16010")      # ada pelanggan: diterima
    await nc.flush()
    await asyncio.sleep(0.2)
    await sub.unsubscribe()
    print("NATS core menerima:", diterima, "(pesan pertama hilang)")


async def demo_jetstream(nc):
    js = nc.jetstream()
    try:
        await js.add_stream(name="TRX", subjects=["trx.>"])
    except BadRequestError:
        # stream sudah ada dengan konfigurasi lain: perbarui
        await js.update_stream(name="TRX", subjects=["trx.>"])

    for _ in range(2):   # kirim dua kali dengan ID sama: hanya satu yang disimpan
        ack = await js.publish("trx.qris", b'{"id_trx":"T-881","nominal":250000}',
                               headers={"Nats-Msg-Id": "T-881"})
        print("seq", ack.seq, "duplikat:", ack.duplicate)

    # durable consumer: posisi baca disimpan server dengan nama "fraud"
    sub = await js.pull_subscribe("trx.qris", durable="fraud")
    try:
        for m in await sub.fetch(10, timeout=2):
            print(m.subject, m.data)
            await m.ack()                      # at-least-once: ack sesudah diproses
    except NatsTimeout:
        print("tidak ada pesan baru untuk consumer 'fraud'")

    info = await js.stream_info("TRX")
    print("isi stream TRX:", info.state.messages, "pesan")


async def main():
    nc = await nats.connect(URL)
    await demo_core(nc)
    await demo_jetstream(nc)
    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
