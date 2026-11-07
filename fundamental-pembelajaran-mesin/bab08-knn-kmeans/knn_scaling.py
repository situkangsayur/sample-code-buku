"""Pengaruh scaling dan k pada kNN, diukur dengan cross-validation (Bab 8, Kode 8.2)."""
from sklearn.datasets import load_wine
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)        # 13 fitur dengan satuan sangat berbeda
cv = StratifiedKFold(10, shuffle=True, random_state=0)

for k in (1, 3, 5, 9, 15, 25):
    tanpa = cross_val_score(KNeighborsClassifier(k), X, y, cv=cv).mean()
    dengan = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(k)),
                             X, y, cv=cv).mean()
    print(f"k={k:2d}  tanpa scaling={tanpa:.3f}  dengan scaling={dengan:.3f}")
