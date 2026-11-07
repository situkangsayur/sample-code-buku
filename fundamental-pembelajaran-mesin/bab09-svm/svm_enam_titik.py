"""SVM hard margin pada enam titik dua dimensi (Bab 9, Kode 9.1).

C yang sangat besar membuat soft margin berperilaku seperti hard margin.
"""
import numpy as np
from sklearn.svm import SVC

X = np.array([[3, 1], [3, -1], [5, 2], [1, 0], [0, 2], [0, -1]], dtype=float)
y = np.array([1, 1, 1, -1, -1, -1])

svm = SVC(kernel="linear", C=1e6).fit(X, y)
w, b = svm.coef_[0], svm.intercept_[0]
print("w =", w.round(3), " b =", round(b, 3))                 # [1, 0], -2
print("lebar margin =", round(2 / np.linalg.norm(w), 3))       # 2
print("support vector:", svm.support_vectors_.tolist())
print("alpha_i * y_i :", svm.dual_coef_.round(3))              # 0.5 (x4), 0.25, 0.25
print("y_i (w.x_i+b) :", (y * (X @ w + b)).round(3))
