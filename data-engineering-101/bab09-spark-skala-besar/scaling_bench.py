"""Kode 9.10: kerangka pengukur strong scaling (Algoritma 9.1).

Menjalankan job yang sama sebagai aplikasi Spark terpisah dengan jumlah core berbeda,
lalu menghitung speedup, efisiensi, dan biaya (core x detik).

    python scaling_bench.py --master spark://spark-master:7077 --data data200m --core 1 2 4
    python scaling_bench.py --master "local[{core}]" --data data --core 1 2 4   # di laptop
"""
import argparse
import csv
import statistics
import subprocess
import time


def jalankan(master: str, core: int, job: str, data: str) -> float:
    m = master.format(core=core)
    perintah = ["spark-submit", "--master", m, "--conf", "spark.eventLog.enabled=true",
                "--conf", "spark.eventLog.dir=file:///tmp/spark-events"]
    if m.startswith("spark://"):
        perintah += ["--total-executor-cores", str(core)]
    t0 = time.perf_counter()
    subprocess.run(perintah + [job, data], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return time.perf_counter() - t0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default="local[{core}]")
    ap.add_argument("--job", default="gold_harian.py")
    ap.add_argument("--data", default="data")
    ap.add_argument("--core", type=int, nargs="+", default=[1, 2, 4])
    ap.add_argument("--ulang", type=int, default=3)
    a = ap.parse_args()
    import os
    os.makedirs("/tmp/spark-events", exist_ok=True)

    hasil = {}
    for core in a.core:
        jalankan(a.master, core, a.job, a.data)                     # pemanasan
        t = [jalankan(a.master, core, a.job, a.data) for _ in range(a.ulang)]
        hasil[core] = (statistics.median(t), min(t), max(t))

    t1 = hasil[a.core[0]][0] * a.core[0]   # anggap baseline linear bila core pertama > 1
    with open("hasil_scaling.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["core", "median_s", "min_s", "max_s", "speedup", "efisiensi", "biaya_core_s"])
        for p, (tp, lo, hi) in hasil.items():
            s = t1 / tp
            print(f"p={p:2d} T={tp:7.1f}s [{lo:.1f}-{hi:.1f}] S={s:5.2f} E={s / p:4.2f} biaya={p * tp:8.0f}")
            w.writerow([p, f"{tp:.2f}", f"{lo:.2f}", f"{hi:.2f}", f"{s:.3f}", f"{s / p:.3f}", f"{p * tp:.0f}"])
