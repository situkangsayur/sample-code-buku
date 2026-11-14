"""Knapsack 0/1 sebagai MILP, diselesaikan scipy.optimize.milp (HiGHS).

Bab 28 buku Algoritma 101 (Kode 28.4). Butuh SciPy 1.9 atau lebih baru:
    pip install scipy
Bila SciPy tidak ada, program memberi tahu lalu berhenti tanpa error.
"""
import sys

W = 10
w = [5, 4, 6, 3]
v = [10, 40, 30, 50]

try:
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
except ImportError:
    print("SciPy tidak terpasang; lewati contoh MILP.")
    sys.exit(0)

c = -np.array(v)                              # milp meminimumkan, jadi nilai dinegatifkan
batas = LinearConstraint([w], -np.inf, W)     # sum w_i x_i <= W
res = milp(c, constraints=[batas], integrality=np.ones(4),
           bounds=Bounds(0, 1))               # x_i bulat di [0, 1], jadi x_i in {0, 1}
x = np.round(res.x).astype(int)
print("status:", res.message)
print("x =", x.tolist(), "nilai =", int(-res.fun))   # x = [0, 1, 0, 1] nilai = 90

# relaksasi LP: x_i boleh pecahan; nilainya sama dengan batas akar 105
rel = milp(c, constraints=[batas], bounds=Bounds(0, 1))
print("relaksasi LP:", [round(float(t), 3) for t in rel.x], "nilai =", round(-rel.fun, 3))

if __name__ == "__main__":
    assert x.tolist() == [0, 1, 0, 1] and int(-res.fun) == 90
    assert abs(-rel.fun - 105) < 1e-6
    print("semua uji lolos")
