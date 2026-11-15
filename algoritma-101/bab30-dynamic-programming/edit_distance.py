"""Edit distance (Levenshtein) dengan tabel D[i][j].

Bab 30 buku Algoritma 101, Algoritma 30.7.
Operasi: sisip, hapus, ganti; masing-masing berbiaya 1.
"""


def edit_tabel(x, y):
    """D[i][j] = biaya minimum mengubah x[1..i] menjadi y[1..j]."""
    m, n = len(x), len(y)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i  # hapus i huruf
    for j in range(n + 1):
        d[0][j] = j  # sisip j huruf
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            beda = 0 if x[i - 1] == y[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1,         # hapus x[i]
                          d[i][j - 1] + 1,         # sisip y[j]
                          d[i - 1][j - 1] + beda)  # ganti atau sama
    return d


def edit_distance(x, y):
    return edit_tabel(x, y)[len(x)][len(y)]


if __name__ == "__main__":
    d = edit_tabel("KUCING", "KANCIL")
    for baris in d:
        print(baris)
    assert edit_distance("KUCING", "KANCIL") == 4
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("", "abc") == 3
    assert edit_distance("RUMAH", "RAMAH") == 1
    print("edit_distance(KUCING, KANCIL) =", edit_distance("KUCING", "KANCIL"))
    print("semua uji lolos")
