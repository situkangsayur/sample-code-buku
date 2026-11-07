"""Melatih CNN kecil dengan PyTorch DistributedDataParallel (DDP) + checkpoint per epoch.

Satu mesin, 2 proses:      torchrun --nproc_per_node=2 ddp_latih.py --epoch 5
Tanpa GPU (CPU, gloo):     torchrun --nproc_per_node=2 ddp_latih.py --thread 2
Satu proses (pembanding):  python ddp_latih.py
Lanjut setelah dimatikan:  jalankan perintah yang sama; checkpoint ckpt.pt dimuat otomatis.
Dataset: MNIST (torchvision); --sintetis untuk data acak tanpa unduhan.
"""
import argparse
import os
import time

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler, TensorDataset


def buat_model() -> nn.Module:
    return nn.Sequential(
        nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(64 * 7 * 7, 128), nn.ReLU(), nn.Linear(128, 10))


def buat_dataset(sintetis: bool):
    if sintetis:
        g = torch.Generator().manual_seed(0)
        x = torch.randn(60_000, 1, 28, 28, generator=g)
        y = torch.randint(0, 10, (60_000,), generator=g)
        return TensorDataset(x, y)
    from torchvision import datasets, transforms
    return datasets.MNIST("data", train=True, download=True, transform=transforms.ToTensor())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--epoch", type=int, default=5)
    ap.add_argument("--batch", type=int, default=64, help="ukuran batch PER PROSES")
    ap.add_argument("--thread", type=int, default=0, help="torch.set_num_threads untuk CPU")
    ap.add_argument("--sintetis", action="store_true")
    ap.add_argument("--ckpt", default="ckpt.pt")
    a = ap.parse_args()

    terdistribusi = "RANK" in os.environ          # diisi torchrun
    pakai_gpu = torch.cuda.is_available()
    if a.thread:
        torch.set_num_threads(a.thread)           # bagi core secara adil antarproses
    if terdistribusi:
        dist.init_process_group(backend="nccl" if pakai_gpu else "gloo")
        rank, world = dist.get_rank(), dist.get_world_size()
        local_rank = int(os.environ["LOCAL_RANK"])
    else:
        rank, world, local_rank = 0, 1, 0
    device = torch.device(f"cuda:{local_rank}" if pakai_gpu else "cpu")
    if pakai_gpu:
        torch.cuda.set_device(device)

    torch.manual_seed(0)                          # bobot awal sama; DDP juga broadcast dari rank 0
    model = buat_model().to(device)
    if terdistribusi:
        model = DDP(model, device_ids=[local_rank] if pakai_gpu else None)
    inti = model.module if terdistribusi else model
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)

    mulai_epoch = 0
    if os.path.exists(a.ckpt):                    # restart dari checkpoint terakhir
        ck = torch.load(a.ckpt, map_location=device)
        inti.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        mulai_epoch = ck["epoch"] + 1
        if rank == 0:
            print(f"lanjut dari epoch {mulai_epoch}")

    ds = buat_dataset(a.sintetis)
    sampler = DistributedSampler(ds, num_replicas=world, rank=rank) if terdistribusi else None
    loader = DataLoader(ds, batch_size=a.batch, sampler=sampler, shuffle=sampler is None)

    for epoch in range(mulai_epoch, a.epoch):
        if sampler:
            sampler.set_epoch(epoch)              # acak ulang konsisten di semua proses
        t0 = time.perf_counter()
        model.train()
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            loss = F.cross_entropy(model(x), y)
            opt.zero_grad()
            loss.backward()                       # all-reduce gradien terjadi di sini (DDP)
            opt.step()
        dt = time.perf_counter() - t0
        if rank == 0:
            print(f"epoch {epoch} loss {loss.item():.4f} waktu {dt:.2f}s world={world}")
            torch.save({"model": inti.state_dict(), "opt": opt.state_dict(), "epoch": epoch},
                       a.ckpt + ".tmp")
            os.replace(a.ckpt + ".tmp", a.ckpt)   # tulis atomik: tidak ada checkpoint setengah jadi
        if terdistribusi:
            dist.barrier()                        # semua menunggu checkpoint selesai
    if terdistribusi:
        dist.destroy_process_group()


if __name__ == "__main__":
    main()
