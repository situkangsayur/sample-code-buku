"""GaussianMixture scikit-learn pada data nasabah sintetis dan pada Iris (Bab 6)."""
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import adjusted_rand_score
from data_nasabah import buat_data

X, y = buat_data()
# tol bawaan 1e-3 (per titik) bisa berhenti di dataran landai; di sini diperketat
gmm = GaussianMixture(n_components=3, covariance_type="full", tol=1e-6,
                      max_iter=500, n_init=5, random_state=0).fit(X)
urut = np.argsort(gmm.means_[:, 0])
print("konvergen:", gmm.converged_, " iterasi:", gmm.n_iter_)
print("bobot   :", gmm.weights_[urut].round(3))
print("rata2   :\n", gmm.means_[urut].round(3))
print(f"logL total: {gmm.score(X) * len(X):.2f}")   # score = rata-rata per titik

# Soft assignment untuk tiga nasabah baru
baru = np.array([[5.9, 33.0],    # saldo ~Rp0,8 juta, 33 transaksi
                 [6.2, 27.0],    # di antara dua segmen
                 [7.3, 11.0]])   # saldo ~Rp20 juta, 11 transaksi
P = gmm.predict_proba(baru)[:, urut]
for b, p in zip(baru, P):
    print(f"nasabah {b}: responsibility = {p.round(3)}")

bawaan = GaussianMixture(3, n_init=5, random_state=0).fit(X)
print(f"dengan tol bawaan: iterasi {bawaan.n_iter_}, logL {bawaan.score(X) * len(X):.2f}")
print("ARI segmen sebenarnya vs GMM:", round(adjusted_rand_score(y, gmm.predict(X)), 3))

# Iris: Gaussian naive Bayes (pakai label) vs GMM (tanpa label)
Xi, yi = load_iris(return_X_y=True)
akurasi = cross_val_score(GaussianNB(), Xi, yi, cv=5).mean()
print(f"Iris, GaussianNB akurasi CV-5   : {akurasi:.3f}")
for cov in ["full", "diag"]:
    g = GaussianMixture(3, covariance_type=cov, n_init=10, random_state=0).fit(Xi)
    print(f"Iris, GMM {cov:4s} tanpa label, ARI: {adjusted_rand_score(yi, g.predict(Xi)):.3f}")
