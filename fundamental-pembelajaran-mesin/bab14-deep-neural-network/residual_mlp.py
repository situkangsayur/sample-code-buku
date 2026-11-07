"""Membandingkan MLP dangkal, MLP dalam polos, dan MLP dalam dengan residual
connection pada Fashion-MNIST dengan anggaran pelatihan yang sama.
Kode 11.3 pada buku. Jalankan: python residual_mlp.py --epoch 5 --seed 0"""
import argparse

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class BlokResidual(nn.Module):
    """y = x + F(x), dengan F = Linear-BN-ReLU-Linear-BN (gaya ResNet)."""

    def __init__(self, lebar):
        super().__init__()
        self.f = nn.Sequential(
            nn.Linear(lebar, lebar), nn.BatchNorm1d(lebar), nn.ReLU(),
            nn.Linear(lebar, lebar), nn.BatchNorm1d(lebar),
        )
        self.akt = nn.ReLU()

    def forward(self, x):
        return self.akt(x + self.f(x))        # jalur identitas + cabang residual


class BlokPolos(nn.Module):
    """Sama persis dengan BlokResidual, tetapi tanpa jalur identitas."""

    def __init__(self, lebar):
        super().__init__()
        self.f = BlokResidual(lebar).f
        self.akt = nn.ReLU()

    def forward(self, x):
        return self.akt(self.f(x))


def buat_model(jenis, n_blok, lebar=256):
    Blok = BlokResidual if jenis == "residual" else BlokPolos
    return nn.Sequential(
        nn.Flatten(), nn.Linear(784, lebar), nn.ReLU(),          # stem
        *[Blok(lebar) for _ in range(n_blok)],                    # badan
        nn.Linear(lebar, 10),                                     # head
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epoch", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.2860,), (0.3530,))])
    latih = datasets.FashionMNIST("data", train=True, download=True, transform=tf)
    uji = datasets.FashionMNIST("data", train=False, download=True, transform=tf)
    dl, dl_uji = DataLoader(latih, 128, shuffle=True), DataLoader(uji, 1000)

    for nama, jenis, n_blok in [("dangkal (1 blok)", "polos", 1),
                                ("dalam polos (20 blok)", "polos", 20),
                                ("dalam residual (20 blok)", "residual", 20)]:
        torch.manual_seed(a.seed)
        model = buat_model(jenis, n_blok)
        n_param = sum(p.numel() for p in model.parameters())
        opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
        for epoch in range(a.epoch):
            model.train()
            total, n = 0.0, 0
            for xb, yb in dl:
                loss = nn.functional.cross_entropy(model(xb), yb)
                opt.zero_grad(); loss.backward(); opt.step()
                total += loss.item() * len(yb); n += len(yb)
        model.eval()
        with torch.no_grad():
            benar = sum((model(xb).argmax(1) == yb).sum().item() for xb, yb in dl_uji)
        print(f"{nama:26s} parameter={n_param:>9,d}  loss latih={total / n:.4f}  akurasi uji={benar / len(uji):.4f}")


if __name__ == "__main__":
    main()
