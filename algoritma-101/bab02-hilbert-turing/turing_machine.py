"""Bab 2: simulator Turing machine satu pita.

Mesin ditulis sebagai tabel transisi:
    (state, simbol_dibaca) -> (state_baru, simbol_ditulis, arah)
arah 'L' (kiri), 'R' (kanan). Simbol kosong ditulis '_'.
"""

KOSONG = "_"

# Mesin penambah satu pada bilangan biner (contoh di Bab 2).
TAMBAH_SATU = {
    ("kanan", "0"): ("kanan", "0", "R"),
    ("kanan", "1"): ("kanan", "1", "R"),
    ("kanan", KOSONG): ("bawa", KOSONG, "L"),
    ("bawa", "1"): ("bawa", "0", "L"),
    ("bawa", "0"): ("selesai", "1", "L"),
    ("bawa", KOSONG): ("selesai", "1", "L"),
}

# Mesin yang tidak pernah berhenti: terus bergerak ke kanan.
TANPA_HENTI = {
    ("jalan", "0"): ("jalan", "0", "R"),
    ("jalan", "1"): ("jalan", "1", "R"),
    ("jalan", KOSONG): ("jalan", KOSONG, "R"),
}


def jalankan(tabel, pita_awal, state_awal, state_henti, batas_langkah=10_000, jejak=None):
    """Jalankan mesin. Kembalikan (isi_pita, banyak_langkah, berhenti?).

    Pita disimpan sebagai dict posisi -> simbol supaya bisa tumbuh ke dua arah.
    batas_langkah diperlukan karena kita tidak dapat mengetahui secara umum
    apakah sebuah mesin akan berhenti (halting problem).
    """
    pita = {i: s for i, s in enumerate(pita_awal)}
    kepala, state, langkah = 0, state_awal, 0
    while state not in state_henti:
        if langkah >= batas_langkah:
            return isi(pita), langkah, False
        dibaca = pita.get(kepala, KOSONG)
        if (state, dibaca) not in tabel:
            break  # tidak ada aturan: mesin berhenti
        state_baru, ditulis, arah = tabel[(state, dibaca)]
        if jejak is not None:
            jejak.append((langkah, state, kepala, dibaca, ditulis, arah, state_baru))
        pita[kepala] = ditulis
        kepala += 1 if arah == "R" else -1
        state = state_baru
        langkah += 1
    return isi(pita), langkah, True


def isi(pita):
    """Isi pita tanpa simbol kosong di ujung kiri dan kanan."""
    if not pita:
        return ""
    lo, hi = min(pita), max(pita)
    return "".join(pita.get(i, KOSONG) for i in range(lo, hi + 1)).strip(KOSONG)


if __name__ == "__main__":
    jejak = []
    hasil, langkah, henti = jalankan(TAMBAH_SATU, "1011", "kanan", {"selesai"}, jejak=jejak)
    for j in jejak:
        print("langkah %d: state=%-6s kepala=%2d baca=%s tulis=%s gerak=%s -> %s" % j)
    print("hasil:", hasil, "langkah:", langkah)
    assert (hasil, langkah, henti) == ("1100", 8, True)

    for n in range(0, 200):
        h, _, ok = jalankan(TAMBAH_SATU, format(n, "b"), "kanan", {"selesai"})
        assert ok and int(h, 2) == n + 1
    assert jalankan(TAMBAH_SATU, "111", "kanan", {"selesai"})[0] == "1000"

    _, langkah, henti = jalankan(TANPA_HENTI, "10", "jalan", {"selesai"}, batas_langkah=1000)
    assert not henti and langkah == 1000
    print("mesin TANPA_HENTI dihentikan paksa setelah", langkah, "langkah")
    print("semua uji lolos")
