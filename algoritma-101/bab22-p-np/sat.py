"""Verifikasi dan brute force SAT (Algoritma 22.1, 29.2; Kode 22.1).

Formula CNF ditulis sebagai list klausa. Setiap klausa adalah list literal:
bilangan k > 0 berarti x_k, bilangan -k berarti (not x_k). Gaya ini sama
dengan format DIMACS yang dipakai SAT solver.
"""


def verifikasi_sat(klausa, nilai):
    """nilai[k] adalah True/False untuk x_k; nilai[0] tidak dipakai."""
    for c in klausa:
        puas = False
        for lit in c:
            v = nilai[abs(lit)]
            if (lit > 0 and v) or (lit < 0 and not v):
                puas = True
                break
        if not puas:
            return False          # satu klausa gagal: sertifikat ditolak
    return True


def brute_force_sat(klausa, n):
    """Coba semua 2^n penugasan. Kembalikan (penugasan, banyak_percobaan)."""
    for mask in range(2 ** n):
        nilai = [None] + [bool((mask >> i) & 1) for i in range(n)]
        if verifikasi_sat(klausa, nilai):
            return nilai, mask + 1
    return None, 2 ** n


PHI = [[1, 2], [-2, 3], [-1, -2], [2, 3]]

if __name__ == "__main__":
    print(verifikasi_sat(PHI, [None, True, False, True]))   # True
    print(verifikasi_sat(PHI, [None, True, True, True]))    # False
    nilai, coba = brute_force_sat(PHI, 3)
    print(nilai[1:], coba)                                  # [True, False, True] 6
    assert verifikasi_sat(PHI, nilai)
    # formula tak terpenuhi: x1 dan (not x1)
    assert brute_force_sat([[1], [-1]], 1) == (None, 2)
    # klausa kosong selalu gagal
    assert not verifikasi_sat([[]], [None])
    print("semua uji lolos")
