"""Grid search C dan gamma untuk SVM RBF, dengan dan tanpa scaling (Bab 9, Kode 9.3)."""
import numpy as np
from sklearn.datasets import make_circles
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_circles(n_samples=400, noise=0.1, factor=0.4, random_state=0)
X[:, 1] *= 1000          # satu fitur bersatuan besar, untuk melihat efek scaling

grid = {"svc__C": 2.0 ** np.arange(-5, 16, 2),
        "svc__gamma": 2.0 ** np.arange(-15, 4, 2)}
cv = StratifiedKFold(5, shuffle=True, random_state=0)

for nama, pipa in {"dengan scaling": make_pipeline(StandardScaler(), SVC(kernel="rbf")),
                   "tanpa scaling": make_pipeline(SVC(kernel="rbf"))}.items():
    gs = GridSearchCV(pipa, grid, cv=cv, n_jobs=-1).fit(X, y)
    terbaik = gs.best_estimator_.named_steps["svc"]
    print(f"{nama:15s} akurasi CV={gs.best_score_:.3f} params={gs.best_params_} "
          f"jumlah SV={terbaik.n_support_.sum()}")
