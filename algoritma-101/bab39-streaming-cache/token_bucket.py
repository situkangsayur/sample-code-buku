"""Bab 39: token bucket untuk rate limiter.

Waktu diberikan sebagai argumen supaya uji dapat diulang (tidak memakai jam sistem).
Jalankan: python3 token_bucket.py
"""


class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity   # isi maksimum (besar burst)
        self.rate = rate           # token per detik
        self.tokens = capacity     # awalnya penuh
        self.last = 0.0

    def allow(self, now, cost=1):
        # isi ulang sesuai waktu yang berlalu, tidak melebihi kapasitas
        elapsed = now - self.last
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


class FixedWindow:
    """Pembanding: hitung permintaan per jendela waktu tetap."""

    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.current, self.count = None, 0

    def allow(self, now):
        w = int(now // self.window)
        if w != self.current:
            self.current, self.count = w, 0
        if self.count < self.limit:
            self.count += 1
            return True
        return False


if __name__ == "__main__":
    tb = TokenBucket(capacity=3, rate=1.0)
    times = [0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.2, 3.0, 3.0, 3.0]
    print(" t    token_sebelum  izin  token_sesudah")
    trace = []
    for t in times:
        before = min(tb.capacity, tb.tokens + (t - tb.last) * tb.rate)
        ok = tb.allow(t)
        trace.append(ok)
        print(f"{t:4.1f}   {before:6.2f}       {'ya ' if ok else 'tdk'}   {tb.tokens:6.2f}")
    assert trace == [True, True, True, False, False, True, False, True, True, False]

    # fixed window membolehkan 2x limit di sekitar batas jendela
    fw = FixedWindow(limit=3, window=1.0)
    burst = [0.9, 0.9, 0.9, 1.0, 1.0, 1.0]
    assert sum(fw.allow(t) for t in burst) == 6
    tb2 = TokenBucket(capacity=3, rate=3.0)
    assert sum(tb2.allow(t) for t in burst) == 3
    print("semua uji token_bucket lolos")
