"""Bab 16: menjumlahkan n bilangan dari list Python dan dari linked list buatan sendiri.

Di Python selisihnya terutama berasal dari biaya mengikuti atribut object, bukan
hanya cache. Angka bergantung mesin.
"""
import statistics
import time

from singly_linked_list import SinglyLinkedList


def sum_list(a):
    t = 0
    for v in a:
        t += v
    return t


def sum_linked(s):
    t = 0
    p = s.head
    while p is not None:
        t += p.value
        p = p.next
    return t


def median(fn, arg):
    ts = []
    for _ in range(5):
        t0 = time.perf_counter()
        fn(arg)
        ts.append(time.perf_counter() - t0)
    return statistics.median(ts)


def main():
    n = 10**6
    a = list(range(n))
    s = SinglyLinkedList()
    for v in a:
        s.push_back(v)
    assert sum_list(a) == sum_linked(s) == n * (n - 1) // 2
    print(f"list   : {median(sum_list, a):.4f} s")
    print(f"linked : {median(sum_linked, s):.4f} s")
    print("semua uji lolos")


if __name__ == "__main__":
    main()
