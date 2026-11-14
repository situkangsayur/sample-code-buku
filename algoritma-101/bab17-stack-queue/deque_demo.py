"""Bab 17: collections.deque sebagai queue, maxlen, dan maksimum jendela geser.

Bagian pengukuran membandingkan list.pop(0) (O(n)) dengan deque.popleft() (O(1)).
Angka waktu bergantung mesin.
"""
import time
from collections import deque


def sliding_max(a, k):
    """Maksimum setiap jendela selebar k, O(n) dengan deque berisi indeks."""
    dq = deque()                      # indeks, nilainya menurun dari depan ke belakang
    out = []
    for i, v in enumerate(a):
        while dq and a[dq[-1]] <= v:
            dq.pop()                  # buang yang lebih kecil dari v
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()              # buang yang sudah keluar jendela
        if i >= k - 1:
            out.append(a[dq[0]])
    return out


def drain_list(n):
    q = list(range(n))
    t0 = time.perf_counter()
    while q:
        q.pop(0)
    return time.perf_counter() - t0


def drain_deque(n):
    q = deque(range(n))
    t0 = time.perf_counter()
    while q:
        q.popleft()
    return time.perf_counter() - t0


def main():
    q = deque()
    q.append("A")
    q.append("B")
    q.appendleft("Z")
    assert list(q) == ["Z", "A", "B"]
    assert q.popleft() == "Z" and q.pop() == "B"

    last3 = deque(maxlen=3)
    for x in range(1, 6):
        last3.append(x)
    assert list(last3) == [3, 4, 5]

    a = [1, 3, -1, -3, 5, 3, 6, 7]
    print("sliding max k=3:", sliding_max(a, 3))   # [3, 3, 5, 5, 6, 7]
    assert sliding_max(a, 3) == [3, 3, 5, 5, 6, 7]
    assert sliding_max([4], 1) == [4]

    for n in [10**4, 5 * 10**4, 10**5]:
        print(f"n={n:>7}  list.pop(0) {drain_list(n):.4f} s  deque.popleft {drain_deque(n):.4f} s")
    print("semua uji lolos")


if __name__ == "__main__":
    main()
