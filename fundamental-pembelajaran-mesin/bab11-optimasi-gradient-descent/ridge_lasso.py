"""Ridge dan lasso: bentuk tertutup ridge dengan NumPy, lalu perbandingan
koefisien dengan scikit-learn. Kode 11.4 pada buku."""
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
n, d = 60, 10
X = rng.normal(size=(n, d))
X[:, 1] = X[:, 0] + rng.normal(scale=0.05, size=n)   # dua fitur nyaris kembar
beta_benar = np.array([3, 0, 0, -2, 0, 0, 0, 1.5, 0, 0])
y = X @ beta_benar + rng.normal(scale=1.0, size=n)
X = StandardScaler().fit_transform(X)                # regularisasi butuh skala seragam


def ridge_tertutup(X, y, lam):
    # intersep tidak dihukum: pusatkan y, lalu selesaikan (X^T X + lam I) b = X^T y
    yc = y - y.mean()
    d = X.shape[1]
    return np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ yc)


np.set_printoptions(precision=2, suppress=True)
print("OLS   :", LinearRegression().fit(X, y).coef_)
# Ridge scikit-learn meminimalkan ||y - Xb||^2 + alpha ||b||^2
print("Ridge :", Ridge(alpha=10.0).fit(X, y).coef_)
print("Ridge (NumPy):", ridge_tertutup(X, y, 10.0))
# Lasso scikit-learn meminimalkan (1/2n)||y - Xb||^2 + alpha ||b||_1
las = Lasso(alpha=0.1).fit(X, y)
print("Lasso :", las.coef_)
print("fitur yang dibuang lasso:", np.where(las.coef_ == 0)[0])
