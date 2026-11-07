"""Kode 3.1: entropy, information gain, dan gain ratio dengan NumPy."""
import numpy as np

def entropy(y):
    # y: array label; hitung proporsi tiap kelas
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return -np.sum(p * np.log2(p))   # p > 0, jadi log aman

def info_gain(x, y):
    # x: kolom atribut, y: label, panjang sama
    sisa = 0.0
    for v in np.unique(x):
        mask = (x == v)
        sisa += mask.mean() * entropy(y[mask])   # bobot |S_v|/|S|
    return entropy(y) - sisa

def split_info(x):
    _, counts = np.unique(x, return_counts=True)
    w = counts / counts.sum()
    return -np.sum(w * np.log2(w))


if __name__ == "__main__":
    outlook = np.array("Sunny Sunny Overcast Rain Rain Rain Overcast "
                       "Sunny Sunny Rain Sunny Overcast Overcast Rain".split())
    play = np.array("No No Yes Yes Yes No Yes No Yes Yes Yes Yes Yes No".split())

    print(f"H(S)          = {entropy(play):.3f}")              # 0.940
    print(f"Gain(Outlook) = {info_gain(outlook, play):.3f}")   # 0.247
    print(f"GainRatio     = {info_gain(outlook, play) / split_info(outlook):.3f}")
