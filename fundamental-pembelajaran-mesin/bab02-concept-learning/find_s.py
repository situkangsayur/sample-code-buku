"""Kode 2.1: algoritma Find-S pada data EnjoySport (tanpa pustaka ML)."""
import csv

KOSONG = "0"   # batasan kosong: tidak ada nilai yang cocok
APA_SAJA = "?"  # batasan apa saja boleh


def baca_data(path):
    with open(path, newline="") as f:
        baris = list(csv.reader(f))
    return [(r[:-1], r[-1] == "Yes") for r in baris[1:]]


def find_s(data):
    h = [KOSONG] * len(data[0][0])          # hipotesis paling khusus
    for x, positif in data:
        if not positif:
            continue                        # contoh negatif diabaikan
        for i, nilai in enumerate(x):
            if h[i] == KOSONG:
                h[i] = nilai                # generalisasi minimal pertama
            elif h[i] != nilai:
                h[i] = APA_SAJA             # nilai berbeda: longgarkan
        print("setelah", x, "->", h)
    return h


def klasifikasi(h, x):
    return all(c == APA_SAJA or c == v for c, v in zip(h, x))


if __name__ == "__main__":
    data = baca_data("enjoysport.csv")
    h = find_s(data)
    hari_baru = ["Sunny", "Warm", "Normal", "Strong", "Cool", "Change"]
    print("h akhir:", h)
    print("hari baru:", "Yes" if klasifikasi(h, hari_baru) else "No")
