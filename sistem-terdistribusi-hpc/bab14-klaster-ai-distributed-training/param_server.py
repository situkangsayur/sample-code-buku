"""Parameter server sederhana dengan Ray actor (regresi linier, NumPy).

Mode sinkron: server menunggu gradien semua worker lalu memperbarui sekali.
Mode asinkron: setiap gradien langsung diterapkan; worker bisa memakai bobot basi (stale).
    python param_server.py --mode sinkron --worker 4
    python param_server.py --mode asinkron --worker 4
"""
import argparse

import numpy as np
import ray

D = 50
rng = np.random.default_rng(0)
W_BENAR = rng.standard_normal(D)


def data(benih: int, n: int = 2000):
    r = np.random.default_rng(benih)
    X = r.standard_normal((n, D))
    return X, X @ W_BENAR + 0.01 * r.standard_normal(n)


@ray.remote
class ParameterServer:
    def __init__(self, lr: float) -> None:
        self.w = np.zeros(D)
        self.lr = lr

    def ambil(self) -> np.ndarray:
        return self.w

    def terapkan(self, *grads) -> np.ndarray:   # satu atau banyak gradien sekaligus
        self.w -= self.lr * np.mean(grads, axis=0)
        return self.w


@ray.remote
class Worker:
    def __init__(self, benih: int) -> None:
        self.X, self.y = data(benih)

    def gradien(self, w: np.ndarray) -> np.ndarray:
        i = np.random.randint(0, len(self.y), 64)          # mini-batch
        X, y = self.X[i], self.y[i]
        return 2 * X.T @ (X @ w - y) / len(y)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["sinkron", "asinkron"], default="sinkron")
    ap.add_argument("--worker", type=int, default=4)
    ap.add_argument("--langkah", type=int, default=300)
    a = ap.parse_args()
    ray.init()
    ps = ParameterServer.remote(lr=0.05)
    ws = [Worker.remote(i) for i in range(a.worker)]
    if a.mode == "sinkron":
        for _ in range(a.langkah):
            w = ps.ambil.remote()
            grads = [x.gradien.remote(w) for x in ws]       # semua pakai bobot yang sama
            ray.get(ps.terapkan.remote(*grads))             # barrier: tunggu semua
    else:
        w = ps.ambil.remote()
        sedang = {x.gradien.remote(w): x for x in ws}
        for _ in range(a.langkah * a.worker):
            selesai, _ = ray.wait(list(sedang))             # siapa pun yang duluan
            x = sedang.pop(selesai[0])
            w = ps.terapkan.remote(selesai[0])              # terapkan langsung
            sedang[x.gradien.remote(w)] = x
    w_akhir = ray.get(ps.ambil.remote())
    print(f"{a.mode}: galat bobot = {np.linalg.norm(w_akhir - W_BENAR):.5f}")


if __name__ == "__main__":
    main()
