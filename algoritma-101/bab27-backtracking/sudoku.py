"""Bab 27: Sudoku dengan backtracking (Algoritma 27.5, Kode 27.5).

Papan 9x9 berupa list of list, 0 = sel kosong. Indeks Python mulai 0.
Versi kedua memilih sel kosong dengan kandidat paling sedikit (MRV).
"""

PUZZLE = [
    "530070000",
    "600195000",
    "098000060",
    "800060003",
    "400803001",
    "700020006",
    "060000280",
    "000419005",
    "000080079",
]


def parse(rows):
    return [[int(ch) for ch in r] for r in rows]


def candidates(g, r, c):
    used = set(g[r]) | {g[i][c] for i in range(9)}
    br, bc = 3 * (r // 3), 3 * (c // 3)
    used |= {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [v for v in range(1, 10) if v not in used]


def solve(g, stats):
    """Backtracking polos: isi sel kosong pertama dari kiri atas."""
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                for v in candidates(g, r, c):
                    stats[0] += 1
                    g[r][c] = v
                    if solve(g, stats):
                        return True
                    g[r][c] = 0          # undo
                return False             # tidak ada nilai yang cocok: mundur
    return True                          # tidak ada sel kosong: selesai


def solve_mrv(g, stats):
    """Pilih sel kosong dengan kandidat paling sedikit lebih dulu."""
    best = None
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                cand = candidates(g, r, c)
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
    if best is None:
        return True
    r, c, cand = best
    for v in cand:
        stats[0] += 1
        g[r][c] = v
        if solve_mrv(g, stats):
            return True
        g[r][c] = 0
    return False


def valid(g):
    units = [g[r] for r in range(9)]
    units += [[g[r][c] for r in range(9)] for c in range(9)]
    units += [[g[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]
              for br in (0, 3, 6) for bc in (0, 3, 6)]
    return all(sorted(u) == list(range(1, 10)) for u in units)


if __name__ == "__main__":
    for f in (solve, solve_mrv):
        g, stats = parse(PUZZLE), [0]
        assert f(g, stats)
        assert valid(g)
        # angka awal tidak berubah
        p = parse(PUZZLE)
        assert all(p[r][c] in (0, g[r][c]) for r in range(9) for c in range(9))
        print(f.__name__, "penempatan dicoba:", stats[0])
    print("".join(map(str, g[0])))   # 534678912
    assert g[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]
    print("semua uji lolos")
