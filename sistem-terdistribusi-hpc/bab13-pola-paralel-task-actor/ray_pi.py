"""Monte Carlo pi dengan Ray task: pola task farm + reduce.

Mengukur strong scaling (total sampel tetap) atau weak scaling (sampel per worker tetap)
dan pengaruh jumlah task. Contoh:
    python ray_pi.py --mode strong --sampel 100000000 --task 64
    python ray_pi.py --mode weak --sampel 25000000 --task 64 --worker 4
Tanpa klaster, ray.init() menyalakan Ray lokal di mesin ini.
"""
import argparse
import random
import statistics
import time

import ray


@ray.remote
def sampel_pi(n: int, benih: int) -> int:
    rng = random.Random(benih)          # benih tetap: task deterministik, aman diulang
    masuk = 0
    for _ in range(n):
        x, y = rng.random(), rng.random()
        masuk += (x * x + y * y <= 1.0)
    return masuk


def jalan(total: int, T: int) -> tuple[float, float]:
    per_task = total // T
    mulai = time.perf_counter()
    refs = [sampel_pi.remote(per_task, i) for i in range(T)]   # kirim semua dulu
    masuk = sum(ray.get(refs))                                 # baru tunggu
    dt = time.perf_counter() - mulai
    return 4 * masuk / (per_task * T), dt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alamat", default=None, help="mis. auto atau ray://localhost:10001")
    ap.add_argument("--mode", choices=["strong", "weak"], default="strong")
    ap.add_argument("--sampel", type=int, default=100_000_000)
    ap.add_argument("--task", type=int, default=64)
    ap.add_argument("--worker", type=int, default=1, help="dipakai mode weak")
    ap.add_argument("--ulang", type=int, default=5)
    a = ap.parse_args()
    ray.init(address=a.alamat)
    total = a.sampel if a.mode == "strong" else a.sampel * a.worker
    jalan(total // 100, a.task)                                # pemanasan
    waktu = []
    for _ in range(a.ulang):
        pi, dt = jalan(total, a.task)
        waktu.append(dt)
    print(f"mode={a.mode} sampel={total} task={a.task} cpu_klaster={ray.cluster_resources().get('CPU')}")
    print(f"pi~{pi:.6f} median={statistics.median(waktu):.3f}s min={min(waktu):.3f}s max={max(waktu):.3f}s")


if __name__ == "__main__":
    main()
