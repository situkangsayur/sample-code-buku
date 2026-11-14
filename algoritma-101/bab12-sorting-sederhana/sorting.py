"""Bab 12: bubble sort, selection sort, insertion sort.

Semua fungsi mengurutkan list a secara menaik di tempat (in-place)
dan mengembalikan jumlah perbandingan serta jumlah tukar/geser
supaya dapat dicocokkan dengan tabel tracing di buku.
Indeks Python mulai 0; pseudocode di buku mulai 1.
Jalankan: python3 sorting.py
"""


def bubble_sort(a):
    n = len(a)
    banding = tukar = 0
    for i in range(n - 1):                 # putaran ke-(i+1)
        ada_tukar = False
        for j in range(n - 1 - i):         # elemen terbesar sudah di ujung
            banding += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                tukar += 1
                ada_tukar = True
        if not ada_tukar:                  # tidak ada tukar: sudah terurut
            break
    return banding, tukar


def selection_sort(a):
    n = len(a)
    banding = tukar = 0
    for i in range(n - 1):
        imin = i
        for j in range(i + 1, n):
            banding += 1
            if a[j] < a[imin]:
                imin = j
        if imin != i:
            a[i], a[imin] = a[imin], a[i]
            tukar += 1
    return banding, tukar


def insertion_sort(a):
    banding = geser = 0
    for i in range(1, len(a)):
        kunci = a[i]
        j = i - 1
        while j >= 0:
            banding += 1
            if a[j] > kunci:               # > (bukan >=) menjaga stabilitas
                a[j + 1] = a[j]            # geser ke kanan
                geser += 1
                j -= 1
            else:
                break
        a[j + 1] = kunci
    return banding, geser


SEMUA = [bubble_sort, selection_sort, insertion_sort]

if __name__ == "__main__":
    contoh = [29, 10, 14, 37, 13]
    for f in SEMUA:
        b = contoh.copy()
        hasil = f(b)
        print("%-15s %s banding/tukar-geser = %s" % (f.__name__, b, hasil))
        assert b == [10, 13, 14, 29, 37]

    # angka yang dipakai di tabel buku
    assert bubble_sort(contoh.copy()) == (10, 5)
    assert selection_sort(contoh.copy()) == (10, 3)
    assert insertion_sort(contoh.copy()) == (8, 5)

    # best case dan worst case
    assert bubble_sort([1, 2, 3, 4, 5]) == (4, 0)      # satu putaran, berhenti
    assert insertion_sort([1, 2, 3, 4, 5]) == (4, 0)
    assert selection_sort([1, 2, 3, 4, 5]) == (10, 0)  # tetap n(n-1)/2
    assert bubble_sort([5, 4, 3, 2, 1]) == (10, 10)
    assert insertion_sort([5, 4, 3, 2, 1]) == (10, 10)
    print("Semua uji sorting.py lolos.")
