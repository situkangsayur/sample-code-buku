"""Bab 20: analisis amortized dengan tiga metode.

1. Counter biner: biaya increment = banyak bit yang dibalik.
   Agregat: total < 2n.  Potential: Phi = banyak bit 1, biaya amortized = 2.
2. Array dinamis berlipat dua dengan Phi = 2*size - capacity: biaya amortized append <= 3.
"""


def increment(bits):
    """Algoritma 20.3. bits[0] adalah bit paling kanan. Mengembalikan banyak bit yang dibalik."""
    i = 0
    flips = 0
    while i < len(bits) and bits[i] == 1:
        bits[i] = 0                 # 1 -> 0
        flips += 1
        i += 1
    if i < len(bits):
        bits[i] = 1                 # 0 -> 1
        flips += 1
    return flips


def counter_trace(n, k):
    bits = [0] * k
    rows, total = [], 0
    for step in range(1, n + 1):
        before_ones = sum(bits)
        c = increment(bits)
        total += c
        phi = sum(bits)
        amortized = c + (phi - before_ones)       # biaya aktual + perubahan potential
        rows.append((step, "".join(map(str, reversed(bits))), c, total, phi, amortized))
    return rows


def dynamic_array_potential(n):
    """Kapasitas awal 0, lalu 1, 2, 4, ... Biaya: 1 tulis + banyak elemen yang disalin."""
    size, cap = 0, 0
    phi_old = 0
    worst_amortized = 0
    total = 0
    for _ in range(n):
        cost = 1
        if size == cap:
            cost += size            # salin semua elemen lama
            cap = 1 if cap == 0 else 2 * cap
        size += 1
        phi = 2 * size - cap
        assert phi >= 0
        amortized = cost + phi - phi_old
        worst_amortized = max(worst_amortized, amortized)
        phi_old = phi
        total += cost
    return total, worst_amortized


if __name__ == "__main__":
    rows = counter_trace(16, 5)
    print("langkah  bit    biaya  total  Phi  amortized")
    for r in rows:
        print(f"{r[0]:>7}  {r[1]}  {r[2]:>5}  {r[3]:>5}  {r[4]:>3}  {r[5]:>9}")
        assert r[5] == 2                         # tidak ada overflow untuk k = 5, n = 16
        assert r[3] < 2 * r[0]
    for n in [10, 1000, 10**5]:
        bits = [0] * 20
        total = sum(increment(bits) for _ in range(n))
        assert total < 2 * n
        print(f"counter n={n:>6}: total balik bit = {total}  (2n = {2*n})")
    for n in [1, 9, 1000, 10**5]:
        total, worst = dynamic_array_potential(n)
        assert worst <= 3 and total < 3 * n
        print(f"array n={n:>6}: total biaya = {total}  amortized terbesar = {worst}")
    print("amortized.py: semua uji lolos")
