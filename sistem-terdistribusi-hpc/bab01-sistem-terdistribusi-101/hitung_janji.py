"""Kode 1.1: availability seri-paralel (Algoritma 1.1), hukum Amdahl, dan Gustafson.

Jalankan: python3 hitung_janji.py
"""


def availability(blok):
    """blok: daftar (a, n) = availability satu replika, jumlah replika."""
    total = 1.0
    for a, n in blok:
        total *= 1 - (1 - a) ** n  # paralel di dalam blok, seri antar blok
    return total


def mtbf_ke_availability(mtbf_jam, mttr_jam):
    return mtbf_jam / (mtbf_jam + mttr_jam)


def amdahl(p, n):
    return 1 / ((1 - p) + p / n)


def gustafson(p, n):
    return (1 - p) + p * n


def downtime_per_tahun(a):
    menit = (1 - a) * 365 * 24 * 60
    return f"{menit / 60:.2f} jam" if menit >= 60 else f"{menit:.1f} menit"


if __name__ == "__main__":
    # jalur pesanan: LB, gateway, layanan pesanan, basis data
    tanpa_replika = [(0.9999, 1), (0.9995, 1), (0.999, 1), (0.999, 1)]
    dengan_replika = [(0.9999, 1), (0.9995, 1), (0.999, 3), (0.999, 2)]
    for nama, jalur in [("tanpa replika", tanpa_replika), ("dengan replika", dengan_replika)]:
        a = availability(jalur)
        print(f"{nama:15s} availability={a:.4%} downtime/tahun={downtime_per_tahun(a)}")

    print(f"MTBF 1000 jam, MTTR 1 jam   -> {mtbf_ke_availability(1000, 1):.4%}")
    print(f"MTBF 1000 jam, MTTR 0.1 jam -> {mtbf_ke_availability(1000, 0.1):.4%}")

    for n in (8, 64, 1024):
        print(f"N={n:5d} amdahl={amdahl(0.95, n):6.2f} gustafson={gustafson(0.95, n):8.2f}")
