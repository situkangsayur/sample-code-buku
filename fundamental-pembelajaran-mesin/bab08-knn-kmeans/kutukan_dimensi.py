"""Simulasi kutukan dimensi: rasio jarak terdekat/terjauh (Bab 8)."""
import numpy as np

rng = np.random.default_rng(0)
for d in (1, 2, 3, 5, 10, 20, 50, 100, 500):
    rasio = []
    for _ in range(200):
        X = rng.random((1000, d))
        q = rng.random(d)
        jarak = np.sqrt(((X - q) ** 2).sum(axis=1))
        rasio.append(jarak.min() / jarak.max())
    print(f"d={d:4d}  d_min/d_max = {np.mean(rasio):.3f}")
