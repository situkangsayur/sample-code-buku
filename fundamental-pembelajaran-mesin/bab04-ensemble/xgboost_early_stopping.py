"""Kode 4.5 - XGBoost dengan early stopping."""
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from data import muat_data

X_tr, X_te, y_tr, y_te, _ = muat_data()

# Sisihkan validation data dari training data (test data tetap utuh)
X_fit, X_val, y_fit, y_val = train_test_split(
    X_tr, y_tr, test_size=0.2, stratify=y_tr, random_state=1)

xgb = XGBClassifier(
    n_estimators=5000, learning_rate=0.05, max_depth=4,
    reg_lambda=1.0, gamma=0.0, subsample=0.8, colsample_bytree=0.8,
    tree_method="hist", eval_metric="logloss",
    early_stopping_rounds=50, n_jobs=-1, random_state=0)
xgb.fit(X_fit, y_fit, eval_set=[(X_val, y_val)], verbose=False)

print("iterasi terbaik =", xgb.best_iteration)
print("XGBoost test acc =", round(xgb.score(X_te, y_te), 4))
