"""Kode 13.2 - Multi-head self-attention dengan PyTorch, plus pengukuran biaya O(n^2)."""
import time

import torch
from torch import nn

n, d_model, h = 6, 512, 8
x = torch.randn(2, n, d_model)                     # batch 2, 6 token
mha = nn.MultiheadAttention(d_model, h, batch_first=True)
print("parameter:", sum(p.numel() for p in mha.parameters()))  # 1050624

mask = torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)  # True = dilarang
z, bobot = mha(x, x, x, attn_mask=mask)
print(z.shape, bobot.shape)
print("bobot token pertama:", bobot[0, 0])

# Waktu dan memori matriks skor tumbuh kuadratik terhadap panjang n (latihan 8)
perangkat = "cuda" if torch.cuda.is_available() else "cpu"
mha = mha.to(perangkat).eval()
with torch.no_grad():
    for n in [128, 256, 512, 1024, 2048]:
        x = torch.randn(1, n, d_model, device=perangkat)
        mulai = time.perf_counter()
        for _ in range(5):
            mha(x, x, x, need_weights=False)
        if perangkat == "cuda":
            torch.cuda.synchronize()
        dt = (time.perf_counter() - mulai) / 5
        mb_skor = h * n * n * 4 / 2**20  # ukuran matriks skor float32 semua head
        print(f"n={n:5d}  waktu {dt*1000:8.2f} ms  matriks skor ~{mb_skor:8.1f} MB")
