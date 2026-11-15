"""DFA yang menerima bilangan biner kelipatan 3 (Algoritma 22.1, Kode 22.1).

State q menyimpan sisa bagi nilai prefiks oleh 3.
Membaca bit b dari state q pindah ke (2q + b) mod 3.
"""


def delta(q, b):
    # fungsi transisi: dua kali nilai lama ditambah bit baru, lalu mod 3
    return (2 * q + b) % 3


def terima_mod3(w):
    q = 0  # state awal q0
    for c in w:
        if c not in "01":
            raise ValueError("simbol di luar alfabet {0,1}")
        q = delta(q, int(c))
    return q == 0  # state terima hanya q0


def jejak(w):
    """Kembalikan daftar state yang dilewati, untuk tabel tracing."""
    q = 0
    hasil = [q]
    for c in w:
        q = delta(q, int(c))
        hasil.append(q)
    return hasil


if __name__ == "__main__":
    print(jejak("1001"))         # [0, 1, 2, 1, 0] -> 1001 = 9, diterima
    print(terima_mod3("1001"))   # True
    print(terima_mod3("1011"))   # False (11)
    for n in range(0, 200):
        assert terima_mod3(format(n, "b")) == (n % 3 == 0)
    assert terima_mod3("")       # string kosong: tetap di q0, diterima
    print("semua uji lolos")
