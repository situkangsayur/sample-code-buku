"""Selang kepercayaan untuk error klasifikasi (Bab 10, Kode 10.1).

Menghitung sample error, standard deviation-nya, dan confidence interval
N persen dengan hampiran normal atas distribusi binomial.
"""
import math

# Pengali z_N untuk beberapa tingkat kepercayaan (dua sisi)
Z = {50: 0.67, 68: 1.00, 80: 1.28, 90: 1.64, 95: 1.96, 98: 2.33, 99: 2.58}


def selang_error(r, n, tingkat=95):
    """r = jumlah salah, n = jumlah data uji yang tidak pernah dipakai latih."""
    err = r / n
    sd = math.sqrt(err * (1 - err) / n)
    z = Z[tingkat]
    return err, sd, (err - z * sd, err + z * sd)


def layak_hampiran_normal(r, n):
    """Patokan praktis: n >= 30 dan n*err*(1-err) >= 5."""
    err = r / n
    return n >= 30 and n * err * (1 - err) >= 5


if __name__ == "__main__":
    err, sd, (lo, hi) = selang_error(12, 40)
    print(f"err={err:.3f} sd={sd:.4f} CI95=[{lo:.3f}; {hi:.3f}]")
    print("hampiran normal layak?", layak_hampiran_normal(12, 40))
    # Lebar selang 95% untuk err = 0,30 pada berbagai n
    for n in (10, 40, 100, 400, 1000, 10000):
        _, _, (lo, hi) = selang_error(0.30 * n, n)
        print(f"n={n:>6}  [{lo:.3f}; {hi:.3f}]  lebar={hi - lo:.3f}")
    # Soal latihan: 27 salah dari 150
    for t in (90, 99):
        err, _, (lo, hi) = selang_error(27, 150, t)
        print(f"27/150 CI{t}=[{lo:.3f}; {hi:.3f}]")
