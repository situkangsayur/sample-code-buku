"""Bab 9: bilangan bulat tanpa batas dan floating point di Python.

Jalankan: python3 bilangan.py
"""
import math
import sys
from fractions import Fraction


def faktorial_iteratif(n):
    hasil = 1
    for i in range(2, n + 1):
        hasil *= i
    return hasil


def hampir_sama(x, y, tol=1e-9):
    """Bandingkan dua float dengan toleransi relatif."""
    return math.isclose(x, y, rel_tol=tol)


def jumlah_sepersepuluh(n):
    """Jumlahkan 0.1 sebanyak n kali."""
    s = 0.0
    for _ in range(n):
        s += 0.1
    return s


if __name__ == "__main__":
    # int Python tidak punya batas atas tetap
    besar = 2 ** 100
    assert besar == 1267650600228229401496703205376
    f30 = faktorial_iteratif(30)
    assert f30 == 265252859812191058636308480000000
    assert len(str(faktorial_iteratif(100))) == 158   # 100! punya 158 digit

    # pembagian
    assert 7 / 2 == 3.5          # / selalu menghasilkan float
    assert 7 // 2 == 3           # // pembagian bulat (floor)
    assert -7 // 2 == -4         # floor, bukan dipotong ke nol
    assert 7 % 3 == 1 and -7 % 3 == 2

    # float adalah biner berpresisi terbatas
    assert 0.1 + 0.2 != 0.3
    assert hampir_sama(0.1 + 0.2, 0.3)
    print("0.1 + 0.2 =", 0.1 + 0.2)                      # 0.30000000000000004
    print("jumlah 0.1 sebanyak 10 kali =", jumlah_sepersepuluh(10))  # 0.9999999999999999
    assert jumlah_sepersepuluh(10) != 1.0
    assert Fraction(1, 10) * 3 == Fraction(3, 10)        # pecahan eksak

    # float punya batas: 2**53 + 1 tidak dapat disimpan tepat
    assert float(2 ** 53) == float(2 ** 53 + 1)
    print("sys.float_info.max =", sys.float_info.max)

    # batas konversi int ke string desimal (Python 3.11 ke atas)
    if hasattr(sys, "get_int_max_str_digits"):
        print("batas digit konversi str:", sys.get_int_max_str_digits())  # 4300
        try:
            str(10 ** 5000)
            print("konversi berhasil (batas dimatikan)")
        except ValueError as e:
            print("ValueError:", str(e)[:60], "...")
        assert len(hex(10 ** 5000)) > 0   # basis 16 tidak dibatasi

    print("Semua uji bilangan.py lolos.")
