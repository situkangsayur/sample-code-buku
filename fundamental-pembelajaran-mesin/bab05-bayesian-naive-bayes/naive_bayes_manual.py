"""Naive Bayes multinomial dari nol untuk korpus email mini (Bab 5, Kode 5.2).

Menghitung dalam ruang log dengan Laplace smoothing, persis seperti contoh
hitungan tangan di Bab 5.
"""
import math
from collections import Counter

latih = [
    ("menang hadiah gratis", "spam"),
    ("gratis hadiah klik sekarang", "spam"),
    ("klik gratis menang", "spam"),
    ("rapat besok pagi", "bukan"),
    ("jadwal rapat proyek", "bukan"),
    ("kirim laporan proyek besok", "bukan"),
]


def latih_nb(data, alpha=1.0):
    kelas = Counter(c for _, c in data)
    hitung = {c: Counter() for c in kelas}
    for teks, c in data:
        hitung[c].update(teks.split())
    kosakata = {w for c in hitung for w in hitung[c]}
    log_prior = {c: math.log(n / len(data)) for c, n in kelas.items()}
    log_lik = {}
    for c in kelas:
        total = sum(hitung[c].values())
        penyebut = total + alpha * len(kosakata)
        log_lik[c] = {w: math.log((hitung[c][w] + alpha) / penyebut) for w in kosakata}
        log_lik[c]["<unk>"] = math.log(alpha / penyebut)
    return log_prior, log_lik


def prediksi(model, teks):
    log_prior, log_lik = model
    skor = {}
    for c in log_prior:
        skor[c] = log_prior[c] + sum(log_lik[c].get(w, log_lik[c]["<unk>"])
                                     for w in teks.split())
    # normalisasi log-sum-exp agar menjadi peluang
    m = max(skor.values())
    z = sum(math.exp(s - m) for s in skor.values())
    return {c: math.exp(s - m) / z for c, s in skor.items()}


if __name__ == "__main__":
    model = latih_nb(latih)
    for email in ("gratis klik hadiah", "gratis rapat besok"):
        print(email, "->", {c: round(p, 3) for c, p in prediksi(model, email).items()})
