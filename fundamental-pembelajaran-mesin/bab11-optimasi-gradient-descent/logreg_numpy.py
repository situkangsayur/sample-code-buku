"""Regresi logistik dari nol dengan gradient descent, dibandingkan dengan
scikit-learn. Kode 11.5 pada buku."""
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def log_loss(p, y, eps=1e-12):
    p = np.clip(p, eps, 1 - eps)          # hindari log(0)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def latih_logistik(X, y, eta=0.1, n_iter=2000, lam=0.0):
    n, d = X.shape
    w, b = np.zeros(d), 0.0
    for t in range(n_iter):
        p = sigmoid(X @ w + b)
        galat = p - y                     # turunan log loss terhadap z
        gw = X.T @ galat / n + lam * w    # suku lam*w = ridge (L2)
        gb = galat.mean()
        w -= eta * gw
        b -= eta * gb
        if t % 500 == 0:
            print(f"iterasi {t:4d}  log loss = {log_loss(p, y):.4f}")
    return w, b


if __name__ == "__main__":
    X, y = load_breast_cancer(return_X_y=True)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
    sk = StandardScaler().fit(Xtr)           # skala dipasang pada data latih saja
    Xtr, Xte = sk.transform(Xtr), sk.transform(Xte)

    w, b = latih_logistik(Xtr, ytr, lam=0.01)
    akurasi = np.mean((sigmoid(Xte @ w + b) >= 0.5) == yte)
    print(f"akurasi uji (NumPy)       : {akurasi:.3f}")

    # C pada scikit-learn = 1 / (lam * n)
    ref = LogisticRegression(C=1 / (0.01 * len(ytr)), max_iter=5000).fit(Xtr, ytr)
    print(f"akurasi uji (scikit-learn): {ref.score(Xte, yte):.3f}")
