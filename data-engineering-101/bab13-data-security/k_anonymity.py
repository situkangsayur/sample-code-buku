"""Menghitung k (k-anonymity) dan l (l-diversity) sebuah tabel."""
import pandas as pd

df = pd.DataFrame({
    "kode_pos": ["16810"] * 3 + ["16911"] * 2,
    "umur": ["30-39"] * 3 + ["40-49"] * 2,
    "jk": ["P"] * 3 + ["L"] * 2,
    "akad": ["Murabahah", "Ijarah", "Murabahah", "Murabahah", "Murabahah"],
})
QI = ["kode_pos", "umur", "jk"]
g = df.groupby(QI)
print("ukuran kelompok:\n", g.size())
print("k =", g.size().min())
print("l =", g["akad"].nunique().min())
