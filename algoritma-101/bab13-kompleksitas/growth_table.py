"""Bab 13: tabel nilai fungsi pertumbuhan dan taksiran waktu pada 10^8 operasi per detik.

Angka 10^8 operasi per detik hanyalah patokan kasar, bukan angka pasti.
"""
import math

OPS_PER_SECOND = 10**8  # asumsi kasar


def growth(n):
    return {
        "1": 1,
        "log n": math.log2(n),
        "n": n,
        "n log n": n * math.log2(n),
        "n^2": n ** 2,
        "n^3": n ** 3,
        "2^n": 2 ** n if n <= 1000 else math.inf,
    }


def human_seconds(ops):
    s = ops / OPS_PER_SECOND
    if s == math.inf:
        return "tak terhingga"
    if s < 1e-3:
        return "< 1 ms"
    if s < 1:
        return f"{s * 1000:.0f} ms"
    if s < 3600:
        return f"{s:.0f} s"
    if s < 86400 * 365:
        return f"{s / 3600:.0f} jam"
    return f"{s / (86400 * 365):.1e} tahun"


def main():
    for n in [10, 1000, 10**6]:
        g = growth(n)
        print(f"n = {n}")
        for name, v in g.items():
            print(f"  {name:8s} {v:>12.4g}  ~ {human_seconds(v)}")
    g = growth(1000)
    assert round(g["log n"], 2) == 9.97
    assert g["n^2"] == 10**6
    assert human_seconds(10**10) == "100 s"
    print("semua uji lolos")


if __name__ == "__main__":
    main()
