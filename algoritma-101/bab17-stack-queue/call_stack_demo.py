"""Bab 17: call stack Python punya batas kedalaman; rekursi terlalu dalam gagal."""
import sys


def hitung_mundur(n):
    if n == 0:
        return 0
    return 1 + hitung_mundur(n - 1)


def hitung_mundur_iteratif(n):
    total = 0
    while n > 0:          # loop tidak menambah frame di call stack
        total += 1
        n -= 1
    return total


def main():
    print("batas rekursi:", sys.getrecursionlimit())     # 1000 (bawaan)
    assert hitung_mundur(500) == 500
    try:
        hitung_mundur(5000)
        failed = False
    except RecursionError as e:
        print("RecursionError:", e)                      # maximum recursion depth exceeded
        failed = True
    assert failed
    assert hitung_mundur_iteratif(5000) == 5000
    print("semua uji lolos")


if __name__ == "__main__":
    main()
