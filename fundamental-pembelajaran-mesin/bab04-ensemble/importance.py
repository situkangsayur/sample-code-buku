"""Kode 4.2 - Feature importance: MDI dibandingkan dengan permutation importance."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

from data import muat_data

X_tr, X_te, y_tr, y_te, names = muat_data()
rf = RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state=42).fit(X_tr, y_tr)

mdi = rf.feature_importances_
# Permutasi dihitung pada data yang TIDAK dipakai melatih
perm = permutation_importance(rf, X_te, y_te, n_repeats=10, random_state=0, n_jobs=-1)

urut = np.argsort(-perm.importances_mean)[:8]
print(f"{'fitur':25s} {'MDI':>7s} {'permutasi':>10s}")
for j in urut:
    print(f"{names[j]:25s} {mdi[j]:7.3f} "
          f"{perm.importances_mean[j]:7.3f} +/- {perm.importances_std[j]:.3f}")

print("\nPeringkat MDI teratas:")
for j in np.argsort(-mdi)[:8]:
    print(f"  {names[j]:25s} {mdi[j]:.3f}")
