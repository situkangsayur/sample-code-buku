"""Bab 16: masalah Josephus dengan circular linked list.

n orang duduk melingkar bernomor 1..n. Mulai dari orang 1, setiap orang ke-k
dikeluarkan. Kembalikan urutan keluar; orang terakhir adalah pemenang.
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def josephus(n, k):
    head = Node(1)
    prev = head
    for i in range(2, n + 1):
        node = Node(i)
        prev.next = node
        prev = node
    prev.next = head                  # tutup lingkaran; prev = orang terakhir
    order = []
    p = prev                          # p menunjuk pendahulu orang yang sedang dihitung
    for _ in range(n):
        for _ in range(k - 1):        # lewati k-1 orang
            p = p.next
        out = p.next
        order.append(out.value)
        p.next = out.next             # keluarkan out dari lingkaran
    return order


def josephus_formula(n, k):
    """Rumus rekursif J(1)=0, J(n)=(J(n-1)+k) mod n, untuk memeriksa pemenang."""
    j = 0
    for m in range(2, n + 1):
        j = (j + k) % m
    return j + 1


def main():
    order = josephus(7, 3)
    print("urutan keluar n=7 k=3:", order)   # [3, 6, 2, 7, 5, 1, 4]
    assert order == [3, 6, 2, 7, 5, 1, 4]
    for n in range(1, 30):
        for k in range(1, 6):
            assert josephus(n, k)[-1] == josephus_formula(n, k)
    print("semua uji lolos")


if __name__ == "__main__":
    main()
