"""Model biaya kasar per jalur (Subbab 11.10). Harga ILUSTRASI dalam rupiah,
bukan harga penyedia tertentu. Jalankan: python biaya.py"""
from dataclasses import dataclass


@dataclass
class Simpan:
    nama: str
    gb: float
    harga_gb_bulan: float
    replikasi: int = 1


@dataclass
class Mesin:
    nama: str
    jumlah: int
    jam_per_bulan: float
    harga_per_jam: float


def biaya_bulanan(simpan: list[Simpan], mesin: list[Mesin], egress: float = 0.0) -> dict:
    s = {x.nama: x.gb * x.replikasi * x.harga_gb_bulan for x in simpan}
    m = {x.nama: x.jumlah * x.jam_per_bulan * x.harga_per_jam for x in mesin}
    total = sum(s.values()) + sum(m.values()) + egress
    return {"simpan": s, "mesin": m, "egress": egress, "total": total}


if __name__ == "__main__":
    hasil = biaya_bulanan(
        simpan=[Simpan("cold_iceberg", 1850, 350),
                Simpan("hot_kafka", 350, 2000, replikasi=3),
                Simpan("hot_clickhouse", 200, 2000)],
        mesin=[Mesin("hot_24jam", 8, 720, 3000),
               Mesin("cold_batch", 6, 90, 3000)])
    for kelompok in ("simpan", "mesin"):
        for k, v in hasil[kelompok].items():
            print(f"{k:15s}: Rp{v:>14,.0f}")
    hot = sum(v for k, v in {**hasil["simpan"], **hasil["mesin"]}.items() if k.startswith("hot"))
    print(f"total          : Rp{hasil['total']:>14,.0f} per bulan")
    print(f"porsi hot      : {hot / hasil['total']:.0%}")
