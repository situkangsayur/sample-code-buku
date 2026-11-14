"""Algoritma 8.1 FaktorialRek dan Kode 8.1: RecursionError untuk n = 5000.
Ditambah JumlahDigit rekursif (Coba Sendiri) dan pangkat cepat rekursif (Subbab 8.5)."""
import math
import sys


def faktorial(n: int) -> int:
    if n == 0:
        return 1                        # kasus basis
    return n * faktorial(n - 1)         # langkah rekursif


def jumlah_digit(n: int) -> int:
    if n < 10:
        return n
    return n % 10 + jumlah_digit(n // 10)


panggilan_pangkat = 0


def pangkat(a: int, n: int) -> int:
    global panggilan_pangkat
    panggilan_pangkat += 1
    if n == 0:
        return 1
    h = pangkat(a, n // 2)              # dipanggil sekali, disimpan di h
    return h * h if n % 2 == 0 else a * h * h


if __name__ == "__main__":
    assert faktorial(4) == 24
    assert faktorial(900) == math.factorial(900)
    assert len(str(faktorial(900))) == 2270
    assert sys.getrecursionlimit() == 1000          # nilai bawaan CPython
    try:
        faktorial(5000)
    except RecursionError as e:
        print("RecursionError:", e)                 # maximum recursion depth exceeded
    else:
        raise AssertionError("seharusnya RecursionError")
    assert jumlah_digit(2026) == 10 and jumlah_digit(0) == 0
    assert pangkat(3, 13) == 3**13 and panggilan_pangkat == 5   # n = 13, 6, 3, 1, 0
    print("faktorial_rek.py: semua uji lolos")
