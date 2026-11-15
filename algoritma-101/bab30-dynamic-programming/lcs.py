"""Longest common subsequence (LCS) dengan tabel L[i][j].

Bab 30 buku Algoritma 101, Algoritma 30.6.
"""


def lcs_tabel(x, y):
    """L[i][j] = panjang LCS dari x[1..i] dan y[1..j] (indeks buku mulai 1)."""
    m, n = len(x), len(y)
    tabel = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:  # string Python mulai 0
                tabel[i][j] = tabel[i - 1][j - 1] + 1
            else:
                tabel[i][j] = max(tabel[i - 1][j], tabel[i][j - 1])
    return tabel


def lcs(x, y):
    """Kembalikan satu LCS dengan menelusuri balik dari L[m][n]."""
    t = lcs_tabel(x, y)
    i, j = len(x), len(y)
    hasil = []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            hasil.append(x[i - 1])
            i -= 1
            j -= 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(hasil))


if __name__ == "__main__":
    t = lcs_tabel("BANDUNG", "BANTEN")
    for baris in t:
        print(baris)
    assert t[7][6] == 4
    assert lcs("BANDUNG", "BANTEN") == "BANN"
    assert lcs("ABCBDAB", "BDCABA") in ("BCBA", "BDAB", "BCAB")
    assert lcs("", "ABC") == ""
    print("LCS(BANDUNG, BANTEN) =", lcs("BANDUNG", "BANTEN"))
    print("semua uji lolos")
