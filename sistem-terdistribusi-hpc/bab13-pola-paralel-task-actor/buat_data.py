"""Membangkitkan banyak berkas CSV transaksi kecil untuk dask_berkas.py."""
import argparse
import os
import random

ap = argparse.ArgumentParser()
ap.add_argument("--berkas", type=int, default=500)
ap.add_argument("--baris", type=int, default=20_000)
a = ap.parse_args()
os.makedirs("data", exist_ok=True)
kanal = ["atm", "mobile", "teller", "qris", "web"]
for i in range(a.berkas):
    rng = random.Random(i)
    with open(f"data/transaksi_{i:04d}.csv", "w") as f:
        f.write("id,kanal,nominal\n")
        for j in range(a.baris):
            f.write(f"{i * a.baris + j},{rng.choice(kanal)},{rng.randint(1, 5000) * 1000}\n")
print(f"selesai: {a.berkas} berkas di data/")
