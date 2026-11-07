"""Memilih tier penyimpanan dari umur dan pola akses data (Kode 1.3).

Aturan sederhana untuk diskusi; angka ambang adalah contoh kebijakan,
bukan ketentuan regulasi.
"""
from dataclasses import dataclass


@dataclass
class Dataset:
    nama: str
    umur_hari: int          # umur data terbaru di dalam dataset
    baca_per_bulan: float   # berapa kali dibaca dalam sebulan terakhir
    butuh_detik: bool       # apakah keputusan bergantung pada data ini dalam hitungan detik
    wajib_simpan: bool      # apakah ada kewajiban retensi (audit, hukum)


def pilih_tier(d: Dataset) -> str:
    if d.butuh_detik:
        return "hot"
    if d.umur_hari <= 400 or d.baca_per_bulan >= 4:
        return "warm"      # dashboard dan rekonsiliasi rutin
    if d.baca_per_bulan >= 0.1:
        return "cold"      # analitik tahunan, data latih model
    return "archive" if d.wajib_simpan else "hapus (habis masa retensi)"


if __name__ == "__main__":
    contoh = [
        Dataset("skor fraud per rekening", 0, 100_000, True, False),
        Dataset("transaksi 13 bulan terakhir", 30, 60, False, True),
        Dataset("transaksi 2023", 1000, 0.5, False, True),
        Dataset("bukti transaksi 2018", 3000, 0.0, False, True),
        Dataset("log klik aplikasi 2019", 2500, 0.0, False, False),
    ]
    for d in contoh:
        print(f"{d.nama:<30} -> {pilih_tier(d)}")
