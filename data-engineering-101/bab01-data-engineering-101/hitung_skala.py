"""Hitungan kasar skala data (Kode 1.1).

Berapa lama membaca 1 TB dari satu disk dan dari banyak disk paralel,
dan berapa volume transaksi bank per hari dan per tahun.
"""

TB = 10**12          # byte, satuan desimal
LAJU_DISK = 200e6    # byte/detik, orde besaran HDD berurutan (ilustrasi)


def waktu_baca(byte: float, jumlah_disk: int, laju: float = LAJU_DISK) -> float:
    """Waktu baca (detik) bila data terbagi rata ke banyak disk yang dibaca paralel."""
    return byte / (laju * jumlah_disk)


def volume_transaksi(nasabah: int, trx_per_hari: float, byte_per_trx: int) -> tuple[float, float]:
    """Volume per hari dan per tahun dalam GB dan TB."""
    per_hari = nasabah * trx_per_hari * byte_per_trx
    return per_hari / 1e9, per_hari * 365 / 1e12


if __name__ == "__main__":
    for n in [1, 10, 100, 1000]:
        t = waktu_baca(TB, n)
        print(f"{n:>5} disk: {t:>8.1f} detik ({t / 60:.1f} menit)")
    gb_hari, tb_tahun = volume_transaksi(1_000_000, 5, 1_000)
    print(f"Transaksi: {gb_hari:.1f} GB/hari, {tb_tahun:.2f} TB/tahun")
