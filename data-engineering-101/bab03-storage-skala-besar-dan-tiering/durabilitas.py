"""Durabilitas replikasi vs erasure coding dengan model sederhana (Kode 3.x).

Asumsi: p = peluang satu potongan hilang sebelum sempat dipulihkan,
kegagalan antarmesin saling bebas (asumsi optimis).
"""
from math import comb


def p_hilang(n: int, toleransi: int, p: float) -> float:
    """Peluang data hilang: lebih dari `toleransi` dari n potongan hilang (binomial eksak)."""
    return sum(comb(n, j) * p**j * (1 - p) ** (n - j) for j in range(toleransi + 1, n + 1))


SKEMA = {
    # nama: (jumlah potongan n, potongan data k)
    "replikasi 3x": (3, 1),
    "RS(6,3)": (9, 6),
    "RS(10,4)": (14, 10),
}

if __name__ == "__main__":
    data_tb = 200
    for p in [1e-2, 1e-3, 1e-4]:
        print(f"p = {p:g}")
        for nama, (n, k) in SKEMA.items():
            tol = n - k                       # potongan yang boleh hilang
            pend = comb(n, tol + 1) * p ** (tol + 1)   # pendekatan suku pertama
            print(f"  {nama:<13} ruang {n / k:.2f}x  kapasitas {data_tb * n / k:>5.0f} TB"
                  f"  tahan {tol}  P_hilang ~ {pend:.2e} (eksak {p_hilang(n, tol, p):.2e})")
