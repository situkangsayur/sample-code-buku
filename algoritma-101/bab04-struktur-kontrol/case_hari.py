"""Kode 4.1: pemilihan case dengan match (Python 3.10 atau lebih baru)."""


def jenis_hari(d: int) -> str:
    match d:
        case 1 | 2 | 3 | 4 | 5:
            return "hari kerja"
        case 6 | 7:
            return "akhir pekan"
        case _:                 # cabang lain: nilai di luar 1..7
            return "tidak valid"


if __name__ == "__main__":
    assert jenis_hari(1) == "hari kerja"
    assert jenis_hari(5) == "hari kerja"
    assert jenis_hari(6) == "akhir pekan"
    assert jenis_hari(7) == "akhir pekan"
    assert jenis_hari(0) == "tidak valid"
    assert jenis_hari(8) == "tidak valid"
    print(jenis_hari(6))        # akhir pekan
    print("case_hari.py: semua uji lolos")
