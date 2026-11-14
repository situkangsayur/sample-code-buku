"""Algoritma 4.2 NilaiHuruf: rangkaian else-if. Skala nilai hanya contoh."""


def nilai_huruf(s: int) -> str:
    if s >= 85:
        return "A"
    elif s >= 70:
        return "B"
    elif s >= 55:
        return "C"
    elif s >= 40:
        return "D"
    else:
        return "E"


if __name__ == "__main__":
    # uji nilai batas di setiap rentang
    harapan = {100: "A", 85: "A", 84: "B", 72: "B", 70: "B", 69: "C",
               55: "C", 54: "D", 40: "D", 39: "E", 0: "E"}
    for s, h in harapan.items():
        assert nilai_huruf(s) == h, (s, nilai_huruf(s), h)
    print("nilai_huruf.py: semua uji lolos")
