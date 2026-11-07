"""Menghitung skor inheren/residual risk register dan membandingkan dengan risk appetite."""
APPETITE = 4
register = [
    # id, risiko, K, D, K_res, D_res
    ("R1", "Bucket terbuka", 3, 5, 1, 5),
    ("R2", "Kredensial di repositori", 4, 4, 1, 4),
    ("R3", "Laporan regulator salah", 3, 4, 1, 4),
    ("R4", "Hapus tak terpenuhi di arsip", 3, 3, 1, 3),
    ("R5", "Ekspor massal orang dalam", 2, 5, 1, 4),
]
for rid, nama, k, d, kr, dr in register:
    inh, res = k * d, kr * dr
    status = "OK" if res <= APPETITE else "DI ATAS APPETITE"
    print(f"{rid} {nama:30s} inheren={inh:2d} residual={res:2d} {status}")
