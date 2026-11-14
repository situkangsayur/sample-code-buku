"""Quick sort dengan partisi Lomuto."""
import random


def partition(a, lo, hi):
    """Partisi Lomuto: pivot = a[hi]. Mengembalikan posisi akhir pivot."""
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def quick_sort(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        p = partition(a, lo, hi)
        quick_sort(a, lo, p - 1)
        quick_sort(a, p + 1, hi)


def randomized_quick_sort(a, lo=0, hi=None):
    """Pivot acak: worst case O(n^2) menjadi sangat tidak mungkin."""
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        r = random.randint(lo, hi)
        a[r], a[hi] = a[hi], a[r]
        p = partition(a, lo, hi)
        randomized_quick_sort(a, lo, p - 1)
        randomized_quick_sort(a, p + 1, hi)


def count_comparisons(a):
    """Banyak perbandingan quick sort (pivot elemen terakhir)."""
    a = list(a)
    total = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo < hi:
            total += hi - lo
            p = partition(a, lo, hi)
            stack.append((lo, p - 1))
            stack.append((p + 1, hi))
    return total


if __name__ == "__main__":
    a = [7, 2, 1, 6, 8, 5, 3, 4]
    p = partition(a, 0, len(a) - 1)
    print(a, p)                      # [2, 1, 3, 4, 8, 5, 7, 6] 3
    assert a == [2, 1, 3, 4, 8, 5, 7, 6] and p == 3
    b = [7, 2, 1, 6, 8, 5, 3, 4]
    quick_sort(b)
    assert b == [1, 2, 3, 4, 5, 6, 7, 8]
    for _ in range(200):
        x = [random.randint(-30, 30) for _ in range(random.randint(0, 50))]
        y, z = list(x), list(x)
        quick_sort(y); randomized_quick_sort(z)
        assert y == sorted(x) and z == sorted(x)
    # worst case: input sudah terurut -> n(n-1)/2 perbandingan
    n = 100
    assert count_comparisons(list(range(n))) == n * (n - 1) // 2
    print("terurut, n=100:", count_comparisons(list(range(n))))
    print("acak,    n=100:", count_comparisons(random.sample(range(n), n)))
    print("semua uji quick sort lolos")
