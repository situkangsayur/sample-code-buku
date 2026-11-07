"""Kode 2.2: Candidate-Elimination untuk hipotesis konjungtif.
Hipotesis berupa tuple; '?' berarti apa saja, '0' berarti kosong."""
from find_s import baca_data

NILAI = [("Sunny", "Cloudy", "Rainy"), ("Warm", "Cold"), ("Normal", "High"),
         ("Strong", "Weak"), ("Warm", "Cool"), ("Same", "Change")]


def cocok(h, x):
    return all(c == "?" or c == v for c, v in zip(h, x))


def lebih_umum(h1, h2):
    # h1 >=g h2 : setiap batasan h1 sama longgar atau lebih longgar
    return all(a == "?" or a == b or b == "0" for a, b in zip(h1, h2))


def generalisasi_min(s, x):
    return tuple(v if c == "0" else (c if c == v else "?") for c, v in zip(s, x))


def spesialisasi_min(g, x):
    hasil = []
    for i, c in enumerate(g):
        if c == "?":
            for v in NILAI[i]:
                if v != x[i]:
                    hasil.append(g[:i] + (v,) + g[i + 1:])
    return hasil


def candidate_elimination(data):
    n = len(NILAI)
    S, G = {("0",) * n}, {("?",) * n}
    for x, positif in data:
        x = tuple(x)
        if positif:
            G = {g for g in G if cocok(g, x)}
            S = {generalisasi_min(s, x) if not cocok(s, x) else s for s in S}
            S = {s for s in S if any(lebih_umum(g, s) for g in G)}
        else:
            S = {s for s in S if not cocok(s, x)}
            G_baru = set()
            for g in G:
                if not cocok(g, x):
                    G_baru.add(g)
                    continue
                for h in spesialisasi_min(g, x):
                    if any(lebih_umum(h, s) for s in S):
                        G_baru.add(h)
            # buang anggota G yang lebih khusus daripada anggota G lain
            G = {g for g in G_baru
                 if not any(g2 != g and lebih_umum(g2, g) for g2 in G_baru)}
        print("S =", sorted(S), "\nG =", sorted(G), "\n")
    return S, G


if __name__ == "__main__":
    candidate_elimination(baca_data("enjoysport.csv"))
