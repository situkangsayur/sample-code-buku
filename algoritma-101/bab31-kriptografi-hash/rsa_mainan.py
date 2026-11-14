"""RSA mainan dengan bilangan kecil (Algoritma 31.1, Kode 31.2).

HANYA untuk belajar. Kunci sekecil ini dapat difaktorkan seketika.
RSA sungguhan memakai modulus 2048 bit atau lebih dan padding (OAEP/PSS)
dari library kriptografi yang sudah diaudit.
"""


def pangkat_mod(b, e, m):
    """Square-and-multiply: b^e mod m dalam O(log e) perkalian."""
    hasil = 1
    b %= m
    while e > 0:
        if e & 1:
            hasil = (hasil * b) % m
        b = (b * b) % m
        e >>= 1
    return hasil


def invers_mod(e, phi):
    """Extended Euclid: cari d dengan (e * d) mod phi = 1."""
    r0, r1 = phi, e
    s0, s1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if r0 != 1:
        raise ValueError("e tidak punya invers modulo phi")
    return s0 % phi


def buat_kunci(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = invers_mod(e, phi)
    return (n, e), (n, d)


def faktorkan_naif(n):
    """Trial division: cepat untuk n kecil, mustahil untuk n 2048 bit."""
    i = 2
    while i * i <= n:
        if n % i == 0:
            return i, n // i
        i += 1
    return None


if __name__ == "__main__":
    publik, privat = buat_kunci(61, 53, 17)
    print(publik, privat)                  # (3233, 17) (3233, 2753)
    m = 65
    c = pangkat_mod(m, publik[1], publik[0])
    print(c)                               # 2790
    print(pangkat_mod(c, privat[1], privat[0]))   # 65
    assert pangkat_mod(c, privat[1], privat[0]) == m
    for m in range(0, 3233):
        c = pangkat_mod(m, 17, 3233)
        assert pangkat_mod(c, 2753, 3233) == m
    assert pangkat_mod(m, 17, 3233) == pow(m, 17, 3233)
    print(faktorkan_naif(3233))            # (53, 61)
    print("semua uji lolos")
