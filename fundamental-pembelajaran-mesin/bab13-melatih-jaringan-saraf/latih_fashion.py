"""Melatih MLP pada Fashion-MNIST dengan praktik lengkap: seed, He init, batch norm,
dropout, AdamW, cosine schedule, augmentasi ringan, early stopping, pencatatan CSV.
Kode 10.5-10.7 pada buku. Jalankan: python latih_fashion.py --epoch 30"""
import argparse
import csv
import random

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


def set_seed(seed):
    # reproduktibilitas: semua sumber acak dikunci
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True, warn_only=True)


def buat_model(lebar=512, p_drop=0.3):
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(784, lebar), nn.BatchNorm1d(lebar), nn.ReLU(), nn.Dropout(p_drop),
        nn.Linear(lebar, lebar // 2), nn.BatchNorm1d(lebar // 2), nn.ReLU(), nn.Dropout(p_drop),
        nn.Linear(lebar // 2, 10),
    )
    for m in model.modules():                      # inisialisasi He untuk ReLU
        if isinstance(m, nn.Linear):
            nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
            nn.init.zeros_(m.bias)
    return model


def data(batch, seed, augmentasi=True):
    norm = transforms.Normalize((0.2860,), (0.3530,))
    tf_latih = [transforms.RandomHorizontalFlip(), transforms.RandomCrop(28, padding=2)] if augmentasi else []
    tf_latih = transforms.Compose(tf_latih + [transforms.ToTensor(), norm])
    tf_uji = transforms.Compose([transforms.ToTensor(), norm])
    # dua objek dataset dengan transformasi berbeda, indeks pembagiannya sama:
    # augmentasi hanya untuk data latih, validasi tidak diaugmentasi
    penuh_aug = datasets.FashionMNIST("data", train=True, download=True, transform=tf_latih)
    penuh_val = datasets.FashionMNIST("data", train=True, download=True, transform=tf_uji)
    idx = torch.randperm(len(penuh_aug), generator=torch.Generator().manual_seed(seed))
    latih, val = Subset(penuh_aug, idx[:55_000].tolist()), Subset(penuh_val, idx[55_000:].tolist())
    uji = datasets.FashionMNIST("data", train=False, download=True, transform=tf_uji)
    g = torch.Generator().manual_seed(seed)
    return (DataLoader(latih, batch, shuffle=True, generator=g),
            DataLoader(val, 1000), DataLoader(uji, 1000))


def evaluasi(model, dl, loss_fn, dev):
    model.eval()                                   # matikan dropout, BN pakai statistik berjalan
    total, benar, jml = 0.0, 0, 0
    with torch.no_grad():
        for xb, yb in dl:
            xb, yb = xb.to(dev), yb.to(dev)
            out = model(xb)
            total += loss_fn(out, yb).item() * len(yb)
            benar += (out.argmax(1) == yb).sum().item()
            jml += len(yb)
    return total / jml, benar / jml


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epoch", type=int, default=30)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--wd", type=float, default=1e-4)
    ap.add_argument("--dropout", type=float, default=0.3)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--sabar", type=int, default=5)   # patience early stopping
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()

    set_seed(a.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    dl_latih, dl_val, dl_uji = data(a.batch, a.seed)
    model = buat_model(p_drop=a.dropout).to(dev)
    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=a.wd)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.epoch)

    terbaik, sabar = float("inf"), 0
    with open("log_pelatihan.csv", "w", newline="") as f:
        log = csv.writer(f)
        log.writerow(["epoch", "lr", "loss_latih", "loss_val", "akurasi_val"])
        for epoch in range(1, a.epoch + 1):
            model.train()
            jumlah, n = 0.0, 0
            for xb, yb in dl_latih:
                xb, yb = xb.to(dev), yb.to(dev)
                loss = loss_fn(model(xb), yb)
                opt.zero_grad()
                loss.backward()
                opt.step()
                jumlah += loss.item() * len(yb); n += len(yb)
            loss_val, akurasi_val = evaluasi(model, dl_val, loss_fn, dev)
            log.writerow([epoch, sched.get_last_lr()[0], jumlah / n, loss_val, akurasi_val])
            print(f"epoch {epoch:2d} latih {jumlah / n:.4f} val {loss_val:.4f} akurasi {akurasi_val:.4f}")
            sched.step()
            if loss_val < terbaik - 1e-4:           # early stopping
                terbaik, sabar = loss_val, 0
                torch.save(model.state_dict(), "model_terbaik.pt")
            else:
                sabar += 1
                if sabar >= a.sabar:
                    print(f"berhenti di epoch {epoch}: loss validasi tidak membaik {a.sabar} epoch")
                    break

    model.load_state_dict(torch.load("model_terbaik.pt"))
    print("akurasi uji model terbaik: %.4f" % evaluasi(model, dl_uji, loss_fn, dev)[1])


if __name__ == "__main__":
    main()
