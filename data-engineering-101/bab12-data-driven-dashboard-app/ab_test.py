"""Analisis eksperimen A/B: SRM, uji dua proporsi, selang kepercayaan,
serta simulasi efek peeking dan banyak metrik."""
import numpy as np
from scipy.stats import chisquare
from statsmodels.stats.proportion import (
    proportions_ztest, confint_proportions_2indep)


def ukuran_sampel(p, delta):
    """Aturan praktis Kohavi dkk.: n ~ 16 p(1-p) / delta^2 per kelompok."""
    return int(np.ceil(16 * p * (1 - p) / delta ** 2))


def analisis(aktifA, nA, aktifB, nB):
    p_srm = chisquare([nA, nB]).pvalue
    if p_srm < 0.001:
        raise SystemExit(f"SRM terdeteksi (p={p_srm:.2e}): periksa penugasan")
    z, p = proportions_ztest([aktifB, aktifA], [nB, nA])
    lo, hi = confint_proportions_2indep(aktifB, nB, aktifA, nA, method="wald")
    return p_srm, p, lo, hi


def simulasi_peeking(rng, ulang=500, langkah=1000, maks=20000, p0=0.40):
    """Data TANPA efek; uji tiap 1000 nasabah, berhenti bila p < 0.05."""
    palsu = 0
    for _ in range(ulang):
        a = rng.binomial(1, p0, maks)
        b = rng.binomial(1, p0, maks)
        for n in range(langkah, maks + 1, langkah):
            _, p = proportions_ztest([b[:n].sum(), a[:n].sum()], [n, n])
            if p < 0.05:
                palsu += 1
                break
    return palsu / ulang


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    print("n per kelompok (p=0.40, delta=0.02):", ukuran_sampel(0.40, 0.02))

    nA, nB = 9_700, 9_500
    aktifA = rng.binomial(1, 0.40, nA).sum()
    aktifB = rng.binomial(1, 0.42, nB).sum()
    p_srm, p, lo, hi = analisis(aktifA, nA, aktifB, nB)
    print(f"SRM p={p_srm:.3f}  uji p={p:.4f}  selisih CI95=[{lo:.2%}, {hi:.2%}]")

    print("Peluang minimal satu dari 20 metrik 'signifikan' kebetulan:",
          f"{1 - 0.95 ** 20:.0%}")
    print("Positif palsu dengan peeking:", f"{simulasi_peeking(rng):.0%}",
          "(tanpa peeking seharusnya sekitar 5%)")
