"""Simpangan baku aktivasi melewati 10 lapisan ReLU untuk tiga skema inisialisasi.
Data untuk Gambar 10.2 di buku. Kode 10.1 pada buku."""
import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(size=(1000, 512))           # 1000 contoh, 512 fitur
skema = {
    "N(0, 0.01^2)": lambda fan_in, fan_out: 0.01,
    "Xavier": lambda fan_in, fan_out: np.sqrt(2.0 / (fan_in + fan_out)),
    "He": lambda fan_in, fan_out: np.sqrt(2.0 / fan_in),
}
for nama, std in skema.items():
    a, hasil = x, []
    for lapis in range(10):
        W = rng.normal(0.0, std(512, 512), size=(512, 512))
        a = np.maximum(a @ W, 0.0)         # ReLU
        hasil.append(a.std())
    print(f"{nama:14s}", " ".join(f"{s:.2e}" for s in hasil))
