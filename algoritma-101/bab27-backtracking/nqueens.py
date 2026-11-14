"""Bab 27: n-Queens dengan backtracking (Algoritma 27.2, Kode 27.1).

Indeks di Python mulai 0; di buku baris dan kolom mulai 1.
col[r] = kolom ratu pada baris r.
"""


def place_ok(col, r, c):
    """Periksa apakah ratu di (r, c) aman terhadap ratu pada baris 0..r-1."""
    for i in range(r):
        if col[i] == c or abs(col[i] - c) == r - i:
            return False
    return True


def queens(n, r=0, col=None, out=None):
    """Kumpulkan semua solusi n-Queens (daftar kolom per baris, mulai 0)."""
    if col is None:
        col, out = [0] * n, []
    if r == n:
        out.append(col[:])          # simpul daun: solusi lengkap
        return out
    for c in range(n):
        if place_ok(col, r, c):     # fungsi pembatas
            col[r] = c
            queens(n, r + 1, col, out)
    return out


def count_fast(n):
    """Hitung solusi dengan himpunan kolom dan diagonal: cek O(1) per sel."""
    cols, d1, d2 = set(), set(), set()

    def go(r):
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or (r - c) in d1 or (r + c) in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c)
            total += go(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c)  # undo
        return total

    return go(0)


def count_nodes(n):
    """Banyak simpul yang dibangkitkan backtracking (termasuk akar)."""
    col = [0] * n
    nodes = 1

    def go(r):
        nonlocal nodes
        if r == n:
            return
        for c in range(n):
            if place_ok(col, r, c):
                nodes += 1
                col[r] = c
                go(r + 1)

    go(0)
    return nodes


def trace4():
    """Urutan percobaan (baris, kolom, status) pada 4-Queens sampai solusi pertama, mulai 1."""
    n, col, log = 4, [0] * 4, []

    def go(r):
        if r == n:
            return True
        for c in range(n):
            ok = place_ok(col, r, c)
            log.append((r + 1, c + 1, "taruh" if ok else "tolak"))
            if ok:
                col[r] = c
                if go(r + 1):
                    return True
        log.append((r + 1, None, "mundur"))
        return False

    go(0)
    return log, [c + 1 for c in col]


if __name__ == "__main__":
    expected = [1, 0, 0, 2, 10, 4, 40, 92, 352, 724]
    for n in range(1, 11):
        assert count_fast(n) == expected[n - 1], n
    sols4 = queens(4)
    assert [[c + 1 for c in s] for s in sols4] == [[2, 4, 1, 3], [3, 1, 4, 2]]
    assert len(queens(8)) == 92
    log, first = trace4()
    assert first == [2, 4, 1, 3]
    for row in log:
        print(row)
    # simpul yang dibangkitkan, dibandingkan dengan 4^4 = 256 penempatan tanpa pemangkasan
    print("simpul 4-Queens:", count_nodes(4))      # 17
    print("simpul 8-Queens:", count_nodes(8))      # 2057
    assert count_nodes(4) == 17
    print("Q(1..10) =", [count_fast(n) for n in range(1, 11)])
    print("semua uji lolos")
