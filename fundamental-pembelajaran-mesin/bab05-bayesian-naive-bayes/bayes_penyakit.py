"""Teorema Bayes pada uji penyakit langka, plus pembaruan bertahap (Bab 5, Kode 5.1)."""


def posterior(prior, sensitivitas, spesifisitas):
    """P(sakit | +) dari prevalensi, sensitivitas, dan spesifisitas."""
    jalur_sakit = prior * sensitivitas               # P(+ | sakit) P(sakit)
    jalur_sehat = (1 - prior) * (1 - spesifisitas)   # P(+ | sehat) P(sehat)
    return jalur_sakit / (jalur_sakit + jalur_sehat)


p = 0.008
for uji in (1, 2, 3):
    p = posterior(p, 0.98, 0.97)   # posterior menjadi prior uji berikutnya
    print(f"setelah {uji} uji positif: P(sakit) = {p:.3f}")

# h_ML vs h_MAP untuk satu hasil positif
lik = {"sakit": 0.98, "sehat": 0.03}
pri = {"sakit": 0.008, "sehat": 0.992}
print("h_ML  =", max(lik, key=lik.get))
print("h_MAP =", max(lik, key=lambda h: lik[h] * pri[h]))
