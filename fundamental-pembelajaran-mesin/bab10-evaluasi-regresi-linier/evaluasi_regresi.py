"""Evaluasi regresi: MSE/MAE/R^2 pada data uji dan 5-fold CV (Bab 10, Kode 10.9)."""
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_diabetes(return_X_y=True)          # 442 pasien, 10 fitur
X_lt, X_uj, y_lt, y_uj = train_test_split(X, y, test_size=0.2, random_state=0)

model = make_pipeline(StandardScaler(), LinearRegression())
cv = KFold(n_splits=5, shuffle=True, random_state=0)
skor = ["neg_mean_squared_error", "neg_mean_absolute_error", "r2"]
for nama, m in [("rata-rata", DummyRegressor()), ("linier", model)]:
    h = cross_validate(m, X_lt, y_lt, cv=cv, scoring=skor, return_train_score=True)
    print(f"{nama:9s} RMSE_cv={np.sqrt(-h['test_neg_mean_squared_error']).mean():5.1f}"
          f"  MAE_cv={-h['test_neg_mean_absolute_error'].mean():5.1f}"
          f"  R2_latih={h['train_r2'].mean():.3f}"
          f"  R2_cv={h['test_r2'].mean():.3f} (sd {h['test_r2'].std(ddof=1):.3f})")

model.fit(X_lt, y_lt)                          # sentuh data uji SEKALI
y_hat = model.predict(X_uj)
print(f"uji: RMSE={np.sqrt(mean_squared_error(y_uj, y_hat)):.1f}"
      f" MAE={mean_absolute_error(y_uj, y_hat):.1f} R2={r2_score(y_uj, y_hat):.3f}")
