"""Kode 11.1: kepatuhan SLO kesegaran dan sisa error budget.
Jalankan: python slo_freshness.py"""
from dataclasses import dataclass

@dataclass
class SLO:
    nama: str
    batas_detik: float      # data dianggap segar bila lag <= batas
    target: float           # misalnya 0.99
    periode_menit: int      # misalnya 30 hari = 43200 menit

def evaluasi(slo: SLO, lag_per_menit: list[float]) -> dict:
    """lag_per_menit: satu sampel SLI (detik) per menit sejak awal periode."""
    buruk = sum(1 for lag in lag_per_menit if lag > slo.batas_detik)
    diamati = len(lag_per_menit)
    budget_total = (1 - slo.target) * slo.periode_menit   # menit
    return {
        "slo": slo.nama,
        "kepatuhan": 1 - buruk / diamati if diamati else 1.0,
        "budget_total_menit": budget_total,
        "budget_terpakai_menit": buruk,
        "budget_sisa_menit": budget_total - buruk,
        "habis": buruk >= budget_total,
    }

if __name__ == "__main__":
    import random
    random.seed(11)
    slo = SLO("dasbor-cabang", batas_detik=120, target=0.99, periode_menit=43200)
    # 12 hari data: lag normal 20-90 detik, sesekali gangguan panjang
    sampel = [random.uniform(20, 90) for _ in range(12 * 1440)]
    for awal in (3000, 9000, 15000):          # tiga gangguan masing-masing 100 menit
        sampel[awal:awal + 100] = [600.0] * 100
    print(evaluasi(slo, sampel))
