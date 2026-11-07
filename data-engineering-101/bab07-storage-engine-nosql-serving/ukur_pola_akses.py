"""Mengukur latensi (P50, P99) pola akses di beberapa store dengan jujur:
pemanasan dulu, banyak ulangan, laporkan persentil, bukan satu angka.
Contoh di sini: point lookup saldo di PostgreSQL dan Redis.
Siapkan tabel rekening(id bigint primary key, saldo numeric) dan key Redis saldo:<id>."""
import random
import statistics
import time

import psycopg
import redis


def ukur(fn, n: int = 2000) -> dict:
    for _ in range(100):                       # pemanasan: cache, koneksi, JIT
        fn()
    t = []
    for _ in range(n):
        a = time.perf_counter()
        fn()
        t.append((time.perf_counter() - a) * 1e3)
    t.sort()
    return {"p50_ms": round(t[n // 2], 3), "p99_ms": round(t[int(n * 0.99)], 3),
            "rata2_ms": round(statistics.mean(t), 3)}


pg = psycopg.connect("postgresql://postgres:lab@localhost/postgres")
rd = redis.Redis()


def saldo_pg():
    rid = random.randint(1, 100_000)
    pg.execute("SELECT saldo FROM rekening WHERE id = %s", (rid,)).fetchone()


def saldo_redis():
    rd.get(f"saldo:{random.randint(1, 100_000)}")


if __name__ == "__main__":
    print("PostgreSQL:", ukur(saldo_pg))
    print("Redis     :", ukur(saldo_redis))
