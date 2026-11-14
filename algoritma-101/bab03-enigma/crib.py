"""Bab 3: menempatkan crib dengan sifat 'tidak ada huruf yang menjadi dirinya sendiri'.

Crib adalah potongan teks asli yang ditebak (misalnya WETTERVORHERSAGE,
'prakiraan cuaca'). Karena Enigma tidak pernah menyandikan huruf menjadi
dirinya sendiri, posisi yang membuat satu huruf crib berimpit dengan huruf
yang sama di ciphertext pasti salah.
"""
from enigma import Enigma


def posisi_mungkin(sandi, crib):
    """Kembalikan daftar posisi awal (mulai 0) yang tidak berbenturan."""
    hasil = []
    for i in range(len(sandi) - len(crib) + 1):
        bentrok = False
        for j in range(len(crib)):
            if sandi[i + j] == crib[j]:
                bentrok = True
                break
        if not bentrok:
            hasil.append(i)
    return hasil


if __name__ == "__main__":
    kunci = dict(urutan=("II", "IV", "V"), cincin="BUL", posisi="RTZ",
                 colokan="AV BS CG DL FU HZ IN KM OW RX")
    asli = "ANXOBERKOMMANDOXWETTERVORHERSAGEXBISKAYA"
    sandi = Enigma(**kunci).sandi(asli)
    print("sandi:", sandi)
    assert sandi == "BTHSJLVHFNLGRLBWUQYFTENUTNCHKKILBLBOLJFG"
    crib = "WETTERVORHERSAGE"
    mungkin = posisi_mungkin(sandi, crib)
    print("posisi dicoba :", len(sandi) - len(crib) + 1)
    print("posisi tersisa:", mungkin)
    assert mungkin == [2, 3, 5, 8, 9, 10, 12, 13, 14, 16, 19, 23, 24]
    assert asli.index(crib) in mungkin  # posisi benar (16) tidak pernah tersingkir
    print("semua uji lolos")
