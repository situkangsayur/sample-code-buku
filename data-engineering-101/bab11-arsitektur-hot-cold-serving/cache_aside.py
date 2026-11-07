"""Kode 11.6: cache-aside dengan TTL ber-jitter dan kunci tunggal (SET NX),
ditambah XFetch (Algoritma 11.2).

Jalankan:
  python cache_aside.py --fake     # memakai fakeredis, tanpa server
  python cache_aside.py            # memakai Redis/Valkey di localhost:6379
"""
import argparse, json, math, random, threading, time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
TTL = 60  # detik
PANGGILAN_SUMBER = 0


def hitung_dari_clickhouse(cabang: str) -> dict:
    global PANGGILAN_SUMBER
    PANGGILAN_SUMBER += 1
    time.sleep(0.08)                      # tiruan kueri agregat 80 ms
    return {"cabang": cabang, "jumlah": random.randint(900, 1300)}


def ringkasan_cabang(cabang: str, coba: int = 50) -> dict:
    kunci, kunci_lock = f"ringkas:{cabang}", f"lock:ringkas:{cabang}"
    for _ in range(coba):
        nilai = r.get(kunci)
        if nilai is not None:                       # hit
            return json.loads(nilai)
        # miss: hanya satu pemanggil yang boleh menghitung ulang
        if r.set(kunci_lock, "1", nx=True, ex=10):
            try:
                hasil = hitung_dari_clickhouse(cabang)
                ttl = TTL + random.randint(0, TTL // 5)   # jitter 0-20%
                r.set(kunci, json.dumps(hasil), ex=ttl)
                return hasil
            finally:
                r.delete(kunci_lock)
        time.sleep(0.02)                  # pemanggil lain menunggu sebentar
    return hitung_dari_clickhouse(cabang)  # cadangan bila lock macet


def invalidasi(cabang: str) -> None:
    """Dipanggil consumer CDC saat ada transaksi baru di cabang ini."""
    r.delete(f"ringkas:{cabang}")


def ambil_xfetch(cabang: str, beta: float = 1.0, ttl: int = TTL) -> dict:
    """Algoritma 11.2: kedaluwarsa dini probabilistik (Vattani dkk., 2015)."""
    kunci = f"xf:{cabang}"
    data = r.get(kunci)
    if data is not None:
        e = json.loads(data)
        acak = 1.0 - random.random()                # (0, 1]
        if time.time() - e["delta"] * beta * math.log(acak) < e["kedaluwarsa"]:
            return e["nilai"]
    t0 = time.time()
    nilai = hitung_dari_clickhouse(cabang)
    delta = time.time() - t0
    r.set(kunci, json.dumps({"nilai": nilai, "delta": delta,
                             "kedaluwarsa": time.time() + ttl}), ex=ttl)
    return nilai


def demo_stampede(n_thread: int = 100) -> None:
    """100 permintaan serentak saat cache kosong: berapa kali sumber dipanggil?"""
    global PANGGILAN_SUMBER
    invalidasi("BDG")
    PANGGILAN_SUMBER = 0
    th = [threading.Thread(target=ringkasan_cabang, args=("BDG",)) for _ in range(n_thread)]
    t0 = time.time()
    for t in th:
        t.start()
    for t in th:
        t.join()
    print(f"{n_thread} permintaan serentak -> sumber dipanggil {PANGGILAN_SUMBER} kali "
          f"({time.time() - t0:.2f} s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fake", action="store_true", help="pakai fakeredis")
    if ap.parse_args().fake:
        import fakeredis
        r = fakeredis.FakeRedis(decode_responses=True)
    demo_stampede()
    t0 = time.perf_counter(); ringkasan_cabang("BDG")
    print(f"permintaan berikutnya (hit): {(time.perf_counter() - t0) * 1000:.2f} ms")
    print("xfetch:", ambil_xfetch("JKT"), ambil_xfetch("JKT"))
