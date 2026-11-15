"""Bab 39: skip list (Pugh 1990) dan sorted set ala Redis (hash + skip list).

Jalankan: python3 skip_list.py
"""
import random

MAX_LEVEL = 16
P = 0.25  # Redis memakai peluang 1/4 untuk naik satu level


class Node:
    def __init__(self, score, member, level):
        self.score = score
        self.member = member
        self.forward = [None] * level
        self.backward = None  # hanya di level 0, untuk membaca terbalik


class SkipList:
    def __init__(self, seed=37):
        self.head = Node(float("-inf"), None, MAX_LEVEL)
        self.level = 1
        self.length = 0
        self.tail = None
        self.rng = random.Random(seed)
        self.steps = 0  # banyak langkah maju, untuk eksperimen

    def random_level(self):
        lvl = 1
        while self.rng.random() < P and lvl < MAX_LEVEL:
            lvl += 1
        return lvl

    @staticmethod
    def less(a, b):
        # urut menurut score, lalu member (sama seperti Redis)
        return (a.score, a.member) < b

    def insert(self, score, member):
        update = [self.head] * MAX_LEVEL
        x = self.head
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] is not None and self.less(x.forward[i], (score, member)):
                x = x.forward[i]
            update[i] = x
        lvl = self.random_level()
        if lvl > self.level:
            self.level = lvl
        node = Node(score, member, lvl)
        for i in range(lvl):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        node.backward = update[0] if update[0] is not self.head else None
        if node.forward[0] is not None:
            node.forward[0].backward = node
        else:
            self.tail = node
        self.length += 1

    def delete(self, score, member):
        update = [self.head] * MAX_LEVEL
        x = self.head
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] is not None and self.less(x.forward[i], (score, member)):
                x = x.forward[i]
            update[i] = x
        x = x.forward[0]
        if x is None or (x.score, x.member) != (score, member):
            return False
        for i in range(len(x.forward)):
            if update[i].forward[i] is x:
                update[i].forward[i] = x.forward[i]
        if x.forward[0] is not None:
            x.forward[0].backward = x.backward
        else:
            self.tail = x.backward
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1
        self.length -= 1
        return True

    def first_ge(self, score):
        """Node pertama dengan score >= score; dipakai untuk range query."""
        x = self.head
        for i in range(self.level - 1, -1, -1):
            while x.forward[i] is not None and x.forward[i].score < score:
                x = x.forward[i]
                self.steps += 1
        return x.forward[0]

    def range_by_score(self, lo, hi):
        out = []
        x = self.first_ge(lo)
        while x is not None and x.score <= hi:
            out.append((x.member, x.score))
            x = x.forward[0]
        return out

    def top(self, k):
        out = []
        x = self.tail
        while x is not None and len(out) < k:
            out.append((x.member, x.score))
            x = x.backward
        return out


class SortedSet:
    """Hash table member->score untuk ZSCORE O(1), skip list untuk urutan."""

    def __init__(self, seed=37):
        self.dict = {}
        self.zsl = SkipList(seed)

    def zadd(self, member, score):
        old = self.dict.get(member)
        if old is not None:
            self.zsl.delete(old, member)
        self.dict[member] = score
        self.zsl.insert(score, member)

    def zscore(self, member):
        return self.dict.get(member)

    def zrangebyscore(self, lo, hi):
        return self.zsl.range_by_score(lo, hi)

    def zrevrange_top(self, k):
        return self.zsl.top(k)


if __name__ == "__main__":
    z = SortedSet()
    for m, s in [("ani", 81), ("budi", 67), ("citra", 92), ("dodi", 74), ("eka", 88)]:
        z.zadd(m, s)
    assert z.zrevrange_top(3) == [("citra", 92), ("eka", 88), ("ani", 81)]
    z.zadd("budi", 95)  # update score: hapus lalu sisip ulang
    assert z.zrevrange_top(2) == [("budi", 95), ("citra", 92)]
    assert z.zscore("dodi") == 74
    assert z.zrangebyscore(75, 90) == [("ani", 81), ("eka", 88)]

    # eksperimen: banyak langkah pencarian tumbuh kira-kira logaritmik
    for n in (1_000, 10_000, 100_000):
        sl = SkipList(seed=1)
        for i in range(n):
            sl.insert(i, f"m{i}")
        sl.steps = 0
        rng = random.Random(2)
        q = 200
        for _ in range(q):
            sl.first_ge(rng.randrange(n))
        print(f"n = {n:>7}: rata-rata langkah maju per pencarian = {sl.steps / q:.1f}, level = {sl.level}")

    # acak: hasil skip list sama dengan sorted()
    rng = random.Random(5)
    sl = SkipList(seed=9)
    data = [(rng.randrange(1000), f"x{i}") for i in range(2000)]
    for s, m in data:
        sl.insert(s, m)
    for s, m in data[:500]:
        assert sl.delete(s, m)
    rest = sorted(data[500:])
    got = []
    x = sl.head.forward[0]
    while x is not None:
        got.append((x.score, x.member))
        x = x.forward[0]
    assert got == rest and sl.length == len(rest)
    print("semua uji skip_list lolos")
