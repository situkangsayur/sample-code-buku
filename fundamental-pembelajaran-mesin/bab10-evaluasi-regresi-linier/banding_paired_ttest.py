"""Membandingkan dua algoritma dengan paired t-test (Bab 10, Kode 10.5).

Kedua model dievaluasi pada lipatan yang SAMA, lalu selisih per lipatan
diuji dengan scipy.stats.ttest_rel.
"""
import numpy as np
from scipy import stats
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)  # lipatan sama

err_pohon = 1 - cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=cv)
err_rf = 1 - cross_val_score(RandomForestClassifier(n_estimators=300, random_state=0),
                             X, y, cv=cv)
d = err_pohon - err_rf
t, p = stats.ttest_rel(err_pohon, err_rf)
print(f"rata-rata error pohon={err_pohon.mean():.3f} rf={err_rf.mean():.3f}")
print(f"selisih rata-rata={d.mean():.4f}  t={t:.2f}  p={p:.4f}")

# Hitungan manual dari contoh di buku (5 lipatan)
d_buku = np.array([0.06, 0.05, 0.04, 0.04, 0.03])
k = len(d_buku)
t_manual = d_buku.mean() / np.sqrt(((d_buku - d_buku.mean()) ** 2).sum() / (k * (k - 1)))
print(f"t contoh buku = {t_manual:.2f}, nilai kritis = {stats.t.ppf(0.975, k - 1):.3f}")
