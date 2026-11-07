"""Protokol evaluasi tanpa kebocoran data (Bab 10, Kode 10.4).

Test set dikunci di awal; seluruh preprocessing masuk ke Pipeline sehingga
statistik scaling hanya dihitung dari lipatan latih.
"""
from sklearn.datasets import load_breast_cancer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (StratifiedKFold, cross_validate,
                                     train_test_split)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)

# 1. Kunci test set sejak awal (stratified agar proporsi kelas terjaga)
X_latih, X_uji, y_latih, y_uji = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# 2. Preprocessing + model dalam satu Pipeline
model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                      LogisticRegression(max_iter=1000))

# 3. Stratified 5-fold hanya pada bagian latih
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
hasil = cross_validate(model, X_latih, y_latih, cv=cv,
                       scoring=["accuracy", "f1", "roc_auc"])
for m in ("accuracy", "f1", "roc_auc"):
    s = hasil["test_" + m]
    print(f"{m:9s} CV: {s.mean():.3f} +/- {s.std(ddof=1):.3f}")

# 4. Latih ulang pada seluruh bagian latih, sentuh test set SEKALI
model.fit(X_latih, y_latih)
print("akurasi uji akhir:", round(model.score(X_uji, y_uji), 3))
