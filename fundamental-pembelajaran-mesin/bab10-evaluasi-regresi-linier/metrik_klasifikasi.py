"""Matriks konfusi, presisi, recall, F1, ROC-AUC, dan PR-AUC (Bab 10, Kode 10.2).

Memakai contoh hitungan tangan di Bab 10: 4 positif dan 6 negatif
dengan skor model yang sudah diketahui.
"""
import numpy as np
from sklearn.metrics import (average_precision_score, confusion_matrix,
                             f1_score, precision_score, recall_score,
                             roc_auc_score, roc_curve, precision_recall_curve)

y_true = np.array([1, 1, 0, 1, 0, 0, 1, 0, 0, 0])
skor = np.array([0.95, 0.85, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10])

# Keputusan dengan threshold 0,5
y_pred = (skor >= 0.5).astype(int)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(f"TP={tp} FN={fn} FP={fp} TN={tn}")
print("presisi =", precision_score(y_true, y_pred))
print("recall  =", recall_score(y_true, y_pred))
print("F1      =", round(f1_score(y_true, y_pred), 4))

# Metrik yang tidak bergantung pada satu threshold
print("ROC-AUC =", round(roc_auc_score(y_true, skor), 4))           # 0.8333
print("AP (PR-AUC) =", round(average_precision_score(y_true, skor), 4))  # 0.8304

fpr, tpr, thr = roc_curve(y_true, skor)
print("titik ROC (FPR, TPR):", list(zip(fpr.round(3), tpr.round(3))))
prec, rec, _ = precision_recall_curve(y_true, skor)
print("titik PR (recall, presisi):", list(zip(rec.round(3), prec.round(3))))

# Kasus penipuan 1:1000 dari Bab 10: akurasi menyesatkan
for nama, (tp_, fn_, fp_, tn_) in {"A": (0, 10, 0, 9990), "B": (8, 2, 90, 9900),
                                    "C": (5, 5, 10, 9980)}.items():
    akurasi = (tp_ + tn_) / (tp_ + tn_ + fp_ + fn_)
    p = tp_ / (tp_ + fp_) if tp_ + fp_ else float("nan")
    r = tp_ / (tp_ + fn_)
    f1 = 2 * p * r / (p + r) if tp_ else 0.0
    print(f"model {nama}: akurasi={akurasi:.4f} presisi={p:.3f} recall={r:.2f} F1={f1:.3f}")
