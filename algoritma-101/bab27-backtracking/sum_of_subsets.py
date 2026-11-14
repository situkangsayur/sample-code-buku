"""Bab 27: sum of subsets dengan backtracking (Algoritma 27.3, Kode 27.3).

w terurut naik. x[i] = 1 bila w[i] diambil. Indeks Python mulai 0.
"""


def sum_of_subsets(w, d):
    """Kembalikan semua himpunan bagian w (sebagai daftar nilai) yang jumlahnya d."""
    w = sorted(w)
    n = len(w)
    out, chosen = [], []
    nodes = 0

    def go(i, s, rest):
        # s = jumlah yang sudah diambil, rest = jumlah w[i..n-1] yang belum diputuskan
        nonlocal nodes
        nodes += 1
        if s == d:
            out.append(chosen[:])
            return
        if i == n:
            return
        # pemangkasan: terlalu besar, atau sisa tidak cukup untuk mencapai d
        if s + w[i] > d or s + rest < d:
            return
        chosen.append(w[i])                 # cabang kiri: ambil w[i]
        go(i + 1, s + w[i], rest - w[i])
        chosen.pop()
        go(i + 1, s, rest - w[i])           # cabang kanan: lewati w[i]

    go(0, 0, sum(w))
    return out, nodes


if __name__ == "__main__":
    sols, nodes = sum_of_subsets([3, 5, 6, 7], 15)
    print(sols, "simpul:", nodes)
    assert sols == [[3, 5, 7]]
    sols, nodes = sum_of_subsets([5, 10, 12, 13, 15, 18], 30)
    print(sols, "simpul:", nodes)
    assert sorted(map(sorted, sols)) == [[5, 10, 15], [5, 12, 13], [12, 18]]
    sols, _ = sum_of_subsets([2, 4, 6], 5)
    assert sols == []
    print("semua uji lolos")
