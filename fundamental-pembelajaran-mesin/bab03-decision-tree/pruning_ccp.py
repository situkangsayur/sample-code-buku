"""Kode 3.5: memilih ccp_alpha dengan cross-validation."""
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          stratify=y, random_state=42)
# 1. Pohon penuh tanpa batasan apa pun
penuh = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
print("penuh :", penuh.tree_.node_count, "node,",
      f"latih={penuh.score(X_tr, y_tr):.3f} uji={penuh.score(X_te, y_te):.3f}")

# 2. Jalur cost-complexity: daftar alpha efektif tempat pohon berubah
jalur = penuh.cost_complexity_pruning_path(X_tr, y_tr)
alphas = jalur.ccp_alphas[:-1]           # alpha terakhir = pohon satu node

# 3. Pilih alpha dengan validasi silang 5-fold pada data latih saja
skor = [cross_val_score(DecisionTreeClassifier(random_state=0, ccp_alpha=a),
                        X_tr, y_tr, cv=5).mean() for a in alphas]
a_best = alphas[max(range(len(skor)), key=skor.__getitem__)]

pangkas = DecisionTreeClassifier(random_state=0, ccp_alpha=a_best).fit(X_tr, y_tr)
print(f"alpha*={a_best:.4f}:", pangkas.tree_.node_count, "node,",
      f"latih={pangkas.score(X_tr, y_tr):.3f} uji={pangkas.score(X_te, y_te):.3f}")
