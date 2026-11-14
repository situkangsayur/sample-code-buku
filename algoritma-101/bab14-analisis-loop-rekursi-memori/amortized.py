"""Bab 14: biaya amortized pada array dinamis yang kapasitasnya dilipatduakan.

Bagian pertama mensimulasikan array dinamis dan menghitung banyak penyalinan elemen.
Bagian kedua melihat kapan list Python benar-benar menambah memori (sys.getsizeof).
Pola pertumbuhan list bergantung pada versi CPython.
"""
import sys


def simulate_doubling(n):
    """Kembalikan total penyalinan saat menambah n elemen ke array berkapasitas awal 1."""
    capacity, size, copies = 1, 0, 0
    for _ in range(n):
        if size == capacity:
            copies += size            # salin semua elemen lama ke tempat baru
            capacity *= 2
        size += 1
    return copies


def list_growth_points(n):
    """Daftar (len, ukuran byte) setiap kali ukuran list berubah."""
    points = []
    lst = []
    last = sys.getsizeof(lst)
    points.append((0, last))
    for i in range(n):
        lst.append(i)
        s = sys.getsizeof(lst)
        if s != last:
            points.append((len(lst), s))
            last = s
    return points


def main():
    for n in [1, 2, 3, 10, 1000, 10**5]:
        copies = simulate_doubling(n)
        assert copies < 2 * n
    print("penyalinan untuk n=1000:", simulate_doubling(1000))   # 1023
    print("penyalinan untuk n=1025:", simulate_doubling(1025))   # 2047
    pts = list_growth_points(100)
    print("CPython", sys.version.split()[0], "titik tumbuh list:", pts)
    # banyak realokasi jauh lebih sedikit daripada banyak append
    assert len(pts) < 20
    print("semua uji lolos")


if __name__ == "__main__":
    main()
