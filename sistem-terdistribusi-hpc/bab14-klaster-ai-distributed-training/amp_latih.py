"""Mixed precision: autocast BF16/FP16 + GradScaler (hanya untuk FP16) di satu GPU.

    python amp_latih.py --dtype bf16
    python amp_latih.py --dtype fp16
    python amp_latih.py --dtype fp32
"""
import argparse
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

ap = argparse.ArgumentParser()
ap.add_argument("--dtype", choices=["fp32", "fp16", "bf16"], default="bf16")
ap.add_argument("--langkah", type=int, default=200)
a = ap.parse_args()
assert torch.cuda.is_available(), "contoh ini butuh GPU"
dev = "cuda"
model = nn.Sequential(nn.Linear(4096, 4096), nn.GELU(), nn.Linear(4096, 4096), nn.GELU(),
                      nn.Linear(4096, 10)).to(dev)            # bobot master tetap FP32
opt = torch.optim.AdamW(model.parameters(), lr=1e-4)
dtype = {"fp16": torch.float16, "bf16": torch.bfloat16}.get(a.dtype)
scaler = torch.amp.GradScaler("cuda", enabled=(a.dtype == "fp16"))  # loss scaling hanya FP16
x = torch.randn(256, 4096, device=dev)
y = torch.randint(0, 10, (256,), device=dev)

torch.cuda.synchronize()
t0 = time.perf_counter()
for _ in range(a.langkah):
    with torch.autocast(device_type="cuda", dtype=dtype, enabled=dtype is not None):
        loss = F.cross_entropy(model(x), y)   # matmul di Tensor Core dengan presisi rendah
    opt.zero_grad(set_to_none=True)
    scaler.scale(loss).backward()             # loss dikali S agar gradien kecil tidak jadi nol
    scaler.step(opt)                          # gradien dibagi S; langkah dilewati bila inf/NaN
    scaler.update()                           # S diturunkan bila overflow, dinaikkan perlahan
torch.cuda.synchronize()
print(f"{a.dtype}: {(time.perf_counter() - t0) / a.langkah * 1000:.2f} ms/langkah, "
      f"loss {loss.item():.4f}, memori puncak {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")
