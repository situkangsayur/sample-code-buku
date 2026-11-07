"""Data bersama untuk contoh Bab 4: Breast Cancer Wisconsin (bawaan scikit-learn)."""
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


def muat_data():
    data = load_breast_cancer()
    X_tr, X_te, y_tr, y_te = train_test_split(
        data.data, data.target, test_size=0.25, stratify=data.target, random_state=42)
    return X_tr, X_te, y_tr, y_te, data.feature_names
