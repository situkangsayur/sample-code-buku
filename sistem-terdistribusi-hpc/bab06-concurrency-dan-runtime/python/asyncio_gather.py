"""Kode 6.13: seratus tugas I/O bersamaan dengan asyncio, dan jebakan memblokir loop.

Pemakaian: python asyncio_gather.py
"""
import asyncio, time


async def ambil(i):
    await asyncio.sleep(1)       # pura-pura menunggu jaringan; giliran dilepas
    return i


async def ambil_salah(i):
    time.sleep(0.02)             # SALAH: memblokir seluruh event loop
    return i


async def main():
    t = time.perf_counter()
    hasil = await asyncio.gather(*(ambil(i) for i in range(100)))
    print(len(hasil), f"tugas benar : {time.perf_counter() - t:.2f} detik")   # sekitar 1 detik

    t = time.perf_counter()
    await asyncio.gather(*(ambil_salah(i) for i in range(100)))
    print(f"100 tugas memblokir: {time.perf_counter() - t:.2f} detik (berurutan!)")

    t = time.perf_counter()
    await asyncio.gather(*(asyncio.to_thread(time.sleep, 0.02) for _ in range(100)))
    print(f"dengan to_thread : {time.perf_counter() - t:.2f} detik")

asyncio.run(main())
