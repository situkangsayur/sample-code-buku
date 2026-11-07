"""Training error dan cross-validation error sebagai fungsi k (Bab 8, data gambar kurva error terhadap k)."""
from sklearn.datasets import make_moons
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

X, y = make_moons(n_samples=200, noise=0.35, random_state=3)
cv = StratifiedKFold(10, shuffle=True, random_state=0)
for k in (1, 3, 5, 7, 9, 13, 19, 27, 39, 55, 75, 99):
    model = KNeighborsClassifier(k)
    latih = 1 - model.fit(X, y).score(X, y)
    val = 1 - cross_val_score(model, X, y, cv=cv).mean()
    print(f"({k},{latih:.3f}) ({k},{val:.3f})")
