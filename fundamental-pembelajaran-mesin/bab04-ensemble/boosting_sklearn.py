"""Kode 4.4 - AdaBoost dan gradient boosting di scikit-learn."""
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

from data import muat_data

X_tr, X_te, y_tr, y_te, _ = muat_data()

# AdaBoost dengan stump (pohon kedalaman 1) sebagai weak learner
ada = AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1),
                         n_estimators=300, learning_rate=0.5, random_state=0)
ada.fit(X_tr, y_tr)
print("AdaBoost  test acc =", round(ada.score(X_te, y_te), 4))

# Gradient boosting dengan early stopping bawaan scikit-learn:
# 10% training data disisihkan sebagai validasi internal
gb = GradientBoostingClassifier(n_estimators=2000, learning_rate=0.05,
                                max_depth=3, subsample=0.8,
                                validation_fraction=0.1,
                                n_iter_no_change=50, random_state=0)
gb.fit(X_tr, y_tr)
print("GB        test acc =", round(gb.score(X_te, y_te), 4),
      " pohon terpakai =", gb.n_estimators_)
