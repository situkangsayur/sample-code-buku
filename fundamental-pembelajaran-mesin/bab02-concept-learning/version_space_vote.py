"""Kode 2.3: List-Then-Eliminate. Enumerasi seluruh hipotesis konjungtif,
sisakan yang konsisten (version space), lalu voting untuk instance baru."""
from itertools import product

from candidate_elimination import NILAI, cocok
from find_s import baca_data


def semua_hipotesis():
    # 4 x 3^5 hipotesis tanpa '0', ditambah satu hipotesis kosong
    pilihan = [list(v) + ["?"] for v in NILAI]
    yield from product(*pilihan)
    yield ("0",) * len(NILAI)


def version_space(data):
    return [h for h in semua_hipotesis()
            if all(cocok(h, x) == positif for x, positif in data)]


if __name__ == "__main__":
    data = baca_data("enjoysport.csv")
    print("jumlah hipotesis semantis:", sum(1 for _ in semua_hipotesis()))
    vs = version_space(data)
    print("ukuran version space:", len(vs))
    for h in vs:
        print("  ", h)
    baru = {"A": ("Sunny", "Warm", "Normal", "Strong", "Cool", "Change"),
            "B": ("Rainy", "Cold", "Normal", "Weak", "Warm", "Same"),
            "C": ("Sunny", "Warm", "Normal", "Weak", "Warm", "Same"),
            "D": ("Sunny", "Cold", "Normal", "Strong", "Warm", "Same")}
    for nama, x in baru.items():
        pos = sum(cocok(h, x) for h in vs)
        print(nama, "positif:", pos, "negatif:", len(vs) - pos)
