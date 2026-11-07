"""Mekanisme Laplace untuk hitungan per kecamatan (ilustrasi; untuk produksi
gunakan pustaka DP yang teruji seperti OpenDP)."""
import numpy as np

rng = np.random.default_rng(7)
hitungan = {"Bogor Barat": 1200, "Dramaga": 340, "Tenjolaya": 4}
eps, sensitivitas = 0.5, 1.0
skala = sensitivitas / eps
print(f"skala b = {skala}, simpangan baku ~ {np.sqrt(2) * skala:.2f}")

rilis = {k: max(0, round(v + rng.laplace(0, skala))) for k, v in hitungan.items()}
print("rilis:", rilis)

# Mengapa ada anggaran privasi: rata-rata 1000 rilis mendekati nilai asli
ulang = [hitungan["Tenjolaya"] + rng.laplace(0, skala) for _ in range(1000)]
print("rata-rata 1000 rilis Tenjolaya:", round(float(np.mean(ulang)), 2))
