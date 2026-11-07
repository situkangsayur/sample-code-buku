"""Naive Bayes kategorikal pada PlayTennis dengan dan tanpa smoothing (Bab 5)."""
from collections import Counter

data = [
    ("Sunny", "Hot", "High", "Weak", "No"), ("Sunny", "Hot", "High", "Strong", "No"),
    ("Overcast", "Hot", "High", "Weak", "Yes"), ("Rain", "Mild", "High", "Weak", "Yes"),
    ("Rain", "Cool", "Normal", "Weak", "Yes"), ("Rain", "Cool", "Normal", "Strong", "No"),
    ("Overcast", "Cool", "Normal", "Strong", "Yes"), ("Sunny", "Mild", "High", "Weak", "No"),
    ("Sunny", "Cool", "Normal", "Weak", "Yes"), ("Rain", "Mild", "Normal", "Weak", "Yes"),
    ("Sunny", "Mild", "Normal", "Strong", "Yes"), ("Overcast", "Mild", "High", "Strong", "Yes"),
    ("Overcast", "Hot", "Normal", "Weak", "Yes"), ("Rain", "Mild", "High", "Strong", "No"),
]
NILAI = [3, 3, 2, 2]  # banyaknya nilai tiap atribut, untuk Laplace


def skor(x, alpha=0.0):
    kelas = Counter(r[-1] for r in data)
    hasil = {}
    for v, nv in kelas.items():
        s = nv / len(data)
        for i, a in enumerate(x):
            n = sum(1 for r in data if r[-1] == v and r[i] == a)
            s *= (n + alpha) / (nv + alpha * NILAI[i])
        hasil[v] = s
    return hasil


x = ("Sunny", "Cool", "High", "Strong")
s = skor(x)
print({v: round(p, 4) for v, p in s.items()})                 # Yes 0.0053, No 0.0206
print("P(No | x) =", round(s["No"] / sum(s.values()), 3))     # 0.795
print("dengan Laplace:", {v: round(p, 4) for v, p in skor(x, 1.0).items()})
