"""Kode 4.1 - OOB error random forest terhadap jumlah pohon."""
from sklearn.ensemble import RandomForestClassifier

from data import muat_data

X_tr, X_te, y_tr, y_te, _ = muat_data()

# warm_start=True: pohon lama dipertahankan, hanya pohon baru yang ditambah
rf = RandomForestClassifier(max_features="sqrt", oob_score=True,
                            warm_start=True, n_jobs=-1, random_state=42)
for B in [25, 50, 100, 200, 400]:
    rf.set_params(n_estimators=B)
    rf.fit(X_tr, y_tr)
    print(f"B={B:4d}  OOB error={1 - rf.oob_score_:.4f}")

# Bandingkan dengan error pada test data (baru disentuh di akhir)
print(f"test error = {1 - rf.score(X_te, y_te):.4f}")
