"""Menggambar roofline sederhana dan titik hasil ukur.

Pemakaian: python roofline.py hasil.csv --puncak 8100 --bw 320
hasil.csv berisi kolom: versi,intensitas,gflops (isi dari pengukuran Anda).
"""
import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("csv")
ap.add_argument("--puncak", type=float, required=True, help="GFLOPS puncak")
ap.add_argument("--bw", type=float, required=True, help="bandwidth memori GB/s")
arg = ap.parse_args()

I = np.logspace(-3, 8, 200, base=2)
atap = np.minimum(arg.puncak, I * arg.bw)
plt.loglog(I, atap, base=2, color="darkgreen", lw=2, label="roofline")
with open(arg.csv) as f:
    for baris in csv.DictReader(f):
        x, y = float(baris["intensitas"]), float(baris["gflops"])
        plt.scatter([x], [y], zorder=3)
        plt.annotate(baris["versi"], (x, y), textcoords="offset points", xytext=(5, -10))
plt.xlabel("arithmetic intensity (FLOP/byte)")
plt.ylabel("GFLOPS")
plt.title(f"ridge point = {arg.puncak / arg.bw:.1f} FLOP/byte")
plt.grid(True, which="both", alpha=0.3)
plt.savefig("roofline.png", dpi=150, bbox_inches="tight")
print("tersimpan: roofline.png")
