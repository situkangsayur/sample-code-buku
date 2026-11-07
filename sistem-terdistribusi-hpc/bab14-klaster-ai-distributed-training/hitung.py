"""Kalkulator perencanaan klaster AI: memori ZeRO, waktu 6ND, bubble pipeline,
MTBF klaster, selang checkpoint, energi dan biaya. Semua angka masukan adalah asumsi Anda.

    python hitung.py --param 70e9 --gpu 64 --token 1e12 --flops-gpu 4e14
"""
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("--param", type=float, default=7e9)
ap.add_argument("--gpu", type=int, default=64)
ap.add_argument("--token", type=float, default=1e12)
ap.add_argument("--flops-gpu", type=float, default=4e14, help="FLOP/s efektif per GPU")
ap.add_argument("--pp", type=int, default=4, help="tahap pipeline")
ap.add_argument("--mikro", type=int, default=32, help="jumlah micro-batch")
ap.add_argument("--mtbf-gpu-jam", type=float, default=43_800)
ap.add_argument("--ckpt-menit", type=float, default=1.0)
ap.add_argument("--kw-gpu", type=float, default=0.7)
ap.add_argument("--pue", type=float, default=1.2)
ap.add_argument("--harga-gpu-jam", type=float, default=2.0, help="USD per GPU-jam (asumsi)")
a = ap.parse_args()
P, N = a.param, a.gpu
print("Memori latih per GPU (tanpa activation), mixed precision + Adam:")
for nama, b in [("DDP", 16 * P), ("ZeRO-1", 4 * P + 12 * P / N),
                ("ZeRO-2", 2 * P + 14 * P / N), ("ZeRO-3/FSDP", 16 * P / N)]:
    print(f"  {nama:12s} {b / 1e9:10.1f} GB")
C = 6 * P * a.token
t = C / (a.flops_gpu * N)
print(f"Komputasi 6ND = {C:.2e} FLOP -> {t / 86400:.1f} hari di {N} GPU (scaling sempurna)")
print(f"Porsi bubble pipeline (p={a.pp}, m={a.mikro}) = {(a.pp - 1) / (a.mikro + a.pp - 1):.1%}")
mtbf = a.mtbf_gpu_jam / N * 60
tau = math.sqrt(2 * a.ckpt_menit * mtbf)
print(f"MTBF klaster ~ {mtbf:.0f} menit; selang checkpoint optimal ~ {tau:.1f} menit")
gpu_jam = N * t / 3600
e = gpu_jam * a.kw_gpu * a.pue
print(f"GPU-jam {gpu_jam:,.0f}; energi ~ {e / 1e3:,.1f} MWh (PUE {a.pue}); "
      f"biaya sewa ~ {gpu_jam * a.harga_gpu_jam:,.0f} USD")
