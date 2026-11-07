"""Kode 4.3 - AdaBoost dengan decision stump dari nol (mereproduksi contoh 10 titik)."""
import numpy as np


def stump_terbaik(x, y, w):
    """Cari ambang dan polaritas dengan error berbobot terkecil."""
    terbaik = (np.inf, None, None)
    for th in np.concatenate(([x.min() - 0.5], np.unique(x) + 0.5)):
        for pol in (1, -1):
            pred = np.where(x <= th, pol, -pol)
            eps = w[pred != y].sum()
            if eps < terbaik[0] - 1e-12:
                terbaik = (eps, th, pol)
    return terbaik


def adaboost(x, y, T):
    n = len(x)
    w = np.full(n, 1.0 / n)            # bobot awal seragam
    model = []
    for t in range(T):
        eps, th, pol = stump_terbaik(x, y, w)
        if eps == 0 or eps >= 0.5:
            break
        alpha = 0.5 * np.log((1 - eps) / eps)
        pred = np.where(x <= th, pol, -pol)
        w = w * np.exp(-alpha * y * pred)
        Z = w.sum()
        w = w / Z                      # normalisasi (bagi dengan Z_t)
        model.append((alpha, th, pol))
        print(f"t={t+1} th={th} pol={pol:+d} eps={eps:.4f} alpha={alpha:.4f} Z={Z:.4f}")
        print("     w =", np.round(w, 4))
    return model


def prediksi(model, x):
    F = sum(a * np.where(x <= th, p, -p) for a, th, p in model)
    return np.sign(F)


if __name__ == "__main__":
    x = np.arange(1, 11)
    y = np.array([1, 1, 1, -1, -1, -1, -1, 1, 1, 1])
    m = adaboost(x, y, T=3)
    print("prediksi:", prediksi(m, x), " akurasi:", (prediksi(m, x) == y).mean())
