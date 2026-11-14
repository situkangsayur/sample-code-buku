"""Bab 14: kompleksitas ruang, membalik list di tempat (O(1) tambahan) dan dengan salinan (O(n))."""


def reverse_in_place(a):
    i, j = 0, len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
    return a


def reverse_copy(a):
    b = [None] * len(a)              # ruang tambahan n sel
    for i in range(len(a)):
        b[len(a) - 1 - i] = a[i]
    return b


def sum_recursive(a, i=0):
    """Ruang O(n) karena kedalaman call stack mencapai n."""
    if i == len(a):
        return 0
    return a[i] + sum_recursive(a, i + 1)


def main():
    assert reverse_in_place([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
    assert reverse_copy([1, 2, 3, 4]) == [4, 3, 2, 1]
    assert reverse_in_place([]) == [] and reverse_copy([7]) == [7]
    assert sum_recursive(list(range(500))) == 124750
    try:
        sum_recursive(list(range(5000)))
        deep_ok = True
    except RecursionError:
        deep_ok = False
    print("rekursi sedalam 5000 berhasil?", deep_ok)   # False pada batas bawaan 1000
    print("semua uji lolos")


if __name__ == "__main__":
    main()
