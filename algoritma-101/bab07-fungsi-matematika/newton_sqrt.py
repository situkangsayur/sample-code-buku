"""Algoritma 7.4 AkarNewton dan versi bilangan bulatnya (kotak Di Lapangan, Subbab 7.4)."""
import math


def akar_newton(a: float, eps: float = 1e-12, maks: int = 100) -> float:
    x = a                        # tebakan awal
    for _ in range(maks):
        baru = (x + a / x) / 2
        if abs(baru - x) < eps:
            return baru
        x = baru
    return x                     # belum konvergen dalam maks ulangan


def iterasi_newton(a: float, x0: float, k: int) -> list[float]:
    xs = [x0]
    for _ in range(k):
        xs.append((xs[-1] + a / xs[-1]) / 2)
    return xs


def isqrt_newton(n: int) -> int:
    """floor(sqrt(n)) tanpa floating point: x <- (x + n div x) div 2 selama x mengecil."""
    if n < 2:
        return n
    x = n // 2 + 1               # tebakan awal >= akar n
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


if __name__ == "__main__":
    xs = iterasi_newton(2.0, 2.0, 4)
    assert xs[1] == 1.5
    assert abs(xs[2] - 1.4166666666666667) < 1e-15
    assert abs(xs[3] - 1.4142156862745099) < 1e-15
    assert abs(xs[4] - math.sqrt(2)) < 1e-11
    assert abs(akar_newton(2.0) - math.sqrt(2)) < 1e-12
    assert abs(akar_newton(10.0) - math.sqrt(10)) < 1e-12
    for n in list(range(10_000)) + [10**30 + 12345, 2**127 - 1]:
        assert isqrt_newton(n) == math.isqrt(n)
    # float tidak cukup untuk n besar: int(math.sqrt(n)) bisa meleset
    n = 10**16 - 1
    assert math.isqrt(n) == 99_999_999 and isqrt_newton(n) == 99_999_999
    assert int(math.sqrt(n)) == 100_000_000      # meleset satu
    print("newton_sqrt.py: semua uji lolos")
