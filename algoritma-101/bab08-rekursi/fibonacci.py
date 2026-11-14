"""Kode 8.2: tiga versi Fibonacci (Algoritma 8.3 FibRek, 8.4 FibIter, dan memoization).
Juga mengukur waktu FibRek untuk Tabel 8.1 (angka bergantung mesin)."""
import math
import time
from functools import cache

panggilan = 0


def fib_rek(n: int) -> int:
    global panggilan
    panggilan += 1
    if n <= 1:
        return n
    return fib_rek(n - 1) + fib_rek(n - 2)


@cache                       # simpan hasil setiap n
def fib_memo(n: int) -> int:
    return n if n <= 1 else fib_memo(n - 1) + fib_memo(n - 2)


def fib_iter(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_polos(n: int) -> int:
    """FibRek tanpa penghitung, untuk mengukur waktu."""
    return n if n <= 1 else fib_polos(n - 1) + fib_polos(n - 2)


if __name__ == "__main__":
    assert fib_rek(20) == 6765 and panggilan == 21891
    assert fib_memo(90) == fib_iter(90) == 2880067194370816120
    for n, f, c in [(5, 5, 15), (10, 55, 177), (20, 6765, 21891), (30, 832040, 2692537)]:
        panggilan = 0
        assert fib_rek(n) == f and panggilan == c == 2 * fib_iter(n + 1) - 1
    assert 2 * fib_iter(36) - 1 == 29860703                  # C(35), tanpa menjalankan fib_rek(35)
    phi = (1 + math.sqrt(5)) / 2
    for n in range(1, 60):
        assert round(phi**n / math.sqrt(5)) == fib_iter(n)  # rumus Binet dibulatkan
    for n in (30, 35):
        t = time.perf_counter()
        fib_polos(n)
        print(f"fib_rek({n}): {time.perf_counter() - t:.2f} detik")
    print("fibonacci.py: semua uji lolos")
