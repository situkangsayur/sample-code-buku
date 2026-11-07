"""Kode 3.2: ID3 rekursif dari nol pada PlayTennis."""
import csv
from collections import Counter

import numpy as np

from entropy_gain import info_gain


def id3(X, y, atribut):
    # X: dict nama_atribut -> array nilai; y: array label
    kelas = Counter(y).most_common()
    if len(kelas) == 1 or not atribut:   # sekelas, atau atribut habis
        return kelas[0][0]
    terbaik = max(atribut, key=lambda a: info_gain(X[a], y))
    sisa = [a for a in atribut if a != terbaik]
    pohon = {terbaik: {}}
    for v in np.unique(X[terbaik]):
        m = X[terbaik] == v
        X_v = {a: X[a][m] for a in sisa}
        pohon[terbaik][v] = id3(X_v, y[m], sisa)
    return pohon

def prediksi(pohon, x):
    # x: dict nama_atribut -> nilai untuk satu hari
    while isinstance(pohon, dict):
        a = next(iter(pohon))            # atribut di simpul ini
        pohon = pohon[a].get(x[a])       # None bila nilai tak pernah dilihat
    return pohon


if __name__ == "__main__":
    with open("playtennis.csv", newline="") as f:
        baris = list(csv.DictReader(f))
    atribut = ["Outlook", "Temperature", "Humidity", "Wind"]
    X = {a: np.array([r[a] for r in baris]) for a in atribut}
    y = np.array([r["PlayTennis"] for r in baris])
    pohon = id3(X, y, atribut)
    print(pohon)
    hari = {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Strong"}
    print("prediksi hari baru:", prediksi(pohon, hari))
