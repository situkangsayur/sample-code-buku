"""Biaya menyimpan 10 TB log transaksi selama 7 tahun pada beberapa skenario tiering (Kode 3.x).

Harga per GB-bulan dan biaya ambil di bawah adalah ILUSTRASI (rasio kasar),
bukan harga penyedia mana pun. Ganti dengan harga terkini sebelum dipakai.
"""
HARGA_SIMPAN = {"hot": 350, "warm": 200, "cold": 70, "archive": 15}   # Rp per GB-bulan
HARGA_AMBIL = {"hot": 0, "warm": 150, "cold": 300, "archive": 400}    # Rp per GB dibaca

GB = 10_000          # 10 TB
BULAN = 84           # 7 tahun


def biaya(jadwal: list[tuple[str, int]], baca_gb_per_bulan: dict[str, float] | None = None) -> float:
    """jadwal: daftar (tier, lama_bulan) berurutan; baca: GB dibaca per bulan dari tiap tier."""
    assert sum(b for _, b in jadwal) == BULAN, "jadwal harus 84 bulan"
    baca_gb_per_bulan = baca_gb_per_bulan or {}
    total = 0.0
    for tier, lama in jadwal:
        total += GB * HARGA_SIMPAN[tier] * lama
        total += baca_gb_per_bulan.get(tier, 0) * HARGA_AMBIL[tier] * lama
    return total


if __name__ == "__main__":
    skenario = {
        "A: semua hot": [("hot", 84)],
        "B: bertingkat": [("hot", 1), ("warm", 12), ("cold", 23), ("archive", 48)],
        "C: tanpa archive": [("hot", 1), ("warm", 12), ("cold", 71)],
    }
    for nama, j in skenario.items():
        print(f"{nama:<18} Rp {biaya(j) / 1e6:>7.1f} juta")
    # Bila tim analitik membaca 1 TB per bulan dari cold dan archive
    baca = {"cold": 1000, "archive": 1000}
    print(f"B + baca 1 TB/bln  Rp {biaya(skenario['B: bertingkat'], baca) / 1e6:>7.1f} juta")
