"""Menjalankan program dengan anggaran langkah (Kode 22.3).

Contoh semi-decidable: bila program berhenti, kita pasti tahu.
Bila belum berhenti sampai anggaran habis, kita hanya bisa berkata
"belum tahu". Programnya: iterasi Collatz dari n.
"""


def jalankan_collatz(n, anggaran):
    langkah = 0
    while n != 1:
        if langkah == anggaran:
            return "belum tahu", langkah
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        langkah += 1
    return "berhenti", langkah


if __name__ == "__main__":
    print(jalankan_collatz(27, 50))    # ('belum tahu', 50)
    print(jalankan_collatz(27, 200))   # ('berhenti', 111)
    assert jalankan_collatz(1, 0) == ("berhenti", 0)
    assert jalankan_collatz(6, 100) == ("berhenti", 8)
    assert jalankan_collatz(27, 111) == ("berhenti", 111)
    assert jalankan_collatz(27, 110) == ("belum tahu", 110)
    print("semua uji lolos")
