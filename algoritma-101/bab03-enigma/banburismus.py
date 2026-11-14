"""Bab 3: skor weight of evidence dalam deciban, gagasan inti Banburismus.

Dua pesan ditumpuk pada suatu pergeseran. Hipotesis H: keduanya 'in depth'
(disandikan dengan posisi rotor yang sama pada bagian yang bertumpuk).
Hipotesis H': tidak in depth (huruf saling acak).

Angka peluang huruf sama di bawah ini mengikuti angka perkiraan untuk lalu
lintas Angkatan Laut Jerman dalam Alexander (sekitar 1945), Cryptographic
History of Work on the German Naval Enigma, hlm. 96 (TNA HW 25/1):
  p_depth  = 1/17  (pesan in depth mewarisi ketidakmerataan huruf bahasa Jerman)
  p_acak   = 1/26  (huruf acak seragam)
Contoh 60 pasangan dengan 7 huruf sama adalah contoh rekaan.
"""
import math

P_DEPTH = 1 / 17
P_ACAK = 1 / 26


def deciban(rasio):
    """Weight of evidence = 10 * log10(rasio peluang), dalam deciban."""
    return 10 * math.log10(rasio)


SKOR_SAMA = deciban(P_DEPTH / P_ACAK)              # sekitar +1.85 db
SKOR_BEDA = deciban((1 - P_DEPTH) / (1 - P_ACAK))  # sekitar -0.09 db


def skor_tumpukan(a, b):
    """Jumlahkan bukti untuk setiap pasangan huruf yang bertumpuk."""
    sama = sum(1 for x, y in zip(a, b) if x == y)
    beda = min(len(a), len(b)) - sama
    return sama, beda, sama * SKOR_SAMA + beda * SKOR_BEDA


if __name__ == "__main__":
    print(f"satu huruf sama : {SKOR_SAMA:+.2f} deciban")
    print(f"satu huruf beda : {SKOR_BEDA:+.3f} deciban")
    assert abs(SKOR_SAMA - 1.845) < 0.001
    assert abs(SKOR_BEDA - (-0.093)) < 0.001

    # Contoh di buku: 60 pasangan bertumpuk, 7 di antaranya huruf sama.
    total = 7 * SKOR_SAMA + 53 * SKOR_BEDA
    faktor = 10 ** (total / 10)
    print(f"7 sama, 53 beda : {total:+.2f} deciban, faktor {faktor:.1f}")
    assert abs(total - 7.99) < 0.01

    # Contoh kecil dua potongan pesan buatan.
    sama, beda, s = skor_tumpukan("QWERTZUIOPASDF", "QXERTYUIQPLSDK")
    print(sama, beda, round(s, 2))
    assert (sama, beda) == (9, 5)
    print("semua uji lolos")
