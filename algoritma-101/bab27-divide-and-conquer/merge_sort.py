"""Merge sort.

Indeks Python mulai 0, pseudocode di buku mulai 1.
"""
import random


def merge(left, right):
    """Menggabungkan dua list terurut menjadi satu list terurut."""
    hasil = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:      # <= menjaga sifat stable
            hasil.append(left[i])
            i += 1
        else:
            hasil.append(right[j])
            j += 1
    hasil.extend(left[i:])           # sisa salah satu list
    hasil.extend(right[j:])
    return hasil


def merge_sort(a):
    if len(a) <= 1:                  # kasus basis
        return list(a)
    mid = len(a) // 2
    left = merge_sort(a[:mid])       # divide + conquer
    right = merge_sort(a[mid:])
    return merge(left, right)        # combine


def merge_sort_count(a):
    """Mengembalikan (list terurut, banyak perbandingan)."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, c1 = merge_sort_count(a[:mid])
    right, c2 = merge_sort_count(a[mid:])
    hasil, i, j, c = [], 0, 0, 0
    while i < len(left) and j < len(right):
        c += 1
        if left[i] <= right[j]:
            hasil.append(left[i]); i += 1
        else:
            hasil.append(right[j]); j += 1
    hasil += left[i:] + right[j:]
    return hasil, c1 + c2 + c


if __name__ == "__main__":
    contoh = [38, 27, 43, 3, 9, 82, 10, 5]
    print(merge_sort(contoh))        # [3, 5, 9, 10, 27, 38, 43, 82]
    assert merge_sort(contoh) == sorted(contoh)
    assert merge([3, 27, 38, 43], [5, 9, 10, 82]) == [3, 5, 9, 10, 27, 38, 43, 82]
    assert merge_sort([]) == [] and merge_sort([1]) == [1]
    for _ in range(200):
        a = [random.randint(-50, 50) for _ in range(random.randint(0, 60))]
        assert merge_sort(a) == sorted(a)
    _, c = merge_sort_count(contoh)
    print("perbandingan:", c)
    # stable: pasangan (kunci, label) dengan kunci sama tetap berurutan
    pasangan = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
    def merge_sort_key(a):
        if len(a) <= 1:
            return list(a)
        m = len(a) // 2
        l, r = merge_sort_key(a[:m]), merge_sort_key(a[m:])
        h, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            if l[i][0] <= r[j][0]:
                h.append(l[i]); i += 1
            else:
                h.append(r[j]); j += 1
        return h + l[i:] + r[j:]
    assert merge_sort_key(pasangan) == [(1, "b"), (1, "d"), (2, "a"), (2, "c")]
    print("semua uji merge sort lolos")
