"""Mesin kebijakan ABAC sederhana untuk akses baris dan kolom."""
from dataclasses import dataclass


@dataclass
class Permintaan:
    peran: str
    cabang_pengguna: str
    cabang_baris: str
    tag_kolom: set[str]
    tujuan: str


def putuskan(p: Permintaan) -> str:
    """Kembalikan 'tolak', 'mask', atau 'izinkan'."""
    if p.peran == "analis" and p.cabang_baris != p.cabang_pengguna:
        return "tolak"
    if "PII.Spesifik" in p.tag_kolom:
        if p.peran == "anti_fraud" and p.tujuan == "investigasi":
            return "izinkan"
        return "mask"
    return "izinkan"


if __name__ == "__main__":
    kasus = [
        Permintaan("analis", "BGR", "BGR", {"PII.Spesifik"}, "laporan"),
        Permintaan("analis", "BGR", "DPK", set(), "laporan"),
        Permintaan("anti_fraud", "PST", "DPK", {"PII.Spesifik"}, "investigasi"),
        Permintaan("analis", "BGR", "BGR", {"Internal"}, "laporan"),
    ]
    for k in kasus:
        print(f"{k.peran:11s} {k.cabang_baris} {sorted(k.tag_kolom)} -> {putuskan(k)}")
