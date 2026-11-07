"""Kode 12.2 dan 12.3 - CNN bergaya LeNet-5 vs MLP pada MNIST (atau CIFAR-10).

Jalankan:
    python cnn_mnist.py                 # MNIST, 5 epoch
    python cnn_mnist.py --data cifar10  # CIFAR-10 (3 kanal, 32x32)
"""
import argparse
import time

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class LeNet(nn.Module):
    def __init__(self, kanal=1, sisi=28, n_kelas=10):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Conv2d(kanal, 6, kernel_size=5, padding=2), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(6, 16, kernel_size=5), nn.ReLU(),
            nn.MaxPool2d(2),
        )
        # ukuran sisi setelah backbone: ((sisi/2) - 4) / 2
        s = (sisi // 2 - 4) // 2
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * s * s, 120), nn.ReLU(),
            nn.Linear(120, 84), nn.ReLU(),
            nn.Linear(84, n_kelas),
        )

    def forward(self, x):
        return self.head(self.backbone(x))


def mlp(kanal=1, sisi=28, n_kelas=10):
    return nn.Sequential(nn.Flatten(), nn.Linear(kanal * sisi * sisi, 128), nn.ReLU(),
                         nn.Linear(128, n_kelas))


def muat_data(nama):
    if nama == "mnist":
        tf = transforms.Compose([transforms.ToTensor(),
                                 transforms.Normalize((0.1307,), (0.3081,))])
        latih = datasets.MNIST("data", train=True, download=True, transform=tf)
        uji = datasets.MNIST("data", train=False, download=True, transform=tf)
        return latih, uji, 1, 28
    tf = transforms.Compose([transforms.ToTensor(),
                             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    latih = datasets.CIFAR10("data", train=True, download=True, transform=tf)
    uji = datasets.CIFAR10("data", train=False, download=True, transform=tf)
    return latih, uji, 3, 32


def latih_dan_uji(model, latih, uji, epoch, perangkat):
    model = model.to(perangkat)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    loader = DataLoader(latih, batch_size=64, shuffle=True)
    mulai = time.time()
    for e in range(epoch):
        model.train()
        for x, y in loader:
            x, y = x.to(perangkat), y.to(perangkat)
            opt.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
        print(f"  epoch {e + 1}: loss terakhir {loss.item():.4f}")
    durasi = time.time() - mulai

    model.eval()
    benar = 0
    with torch.no_grad():
        for x, y in DataLoader(uji, batch_size=512):
            x, y = x.to(perangkat), y.to(perangkat)
            benar += (model(x).argmax(1) == y).sum().item()
    return benar / len(uji), durasi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", choices=["mnist", "cifar10"], default="mnist")
    ap.add_argument("--epoch", type=int, default=5)
    a = ap.parse_args()

    torch.manual_seed(42)
    perangkat = "cuda" if torch.cuda.is_available() else "cpu"
    latih, uji, kanal, sisi = muat_data(a.data)

    for nama, model in [("CNN (LeNet)", LeNet(kanal, sisi)), ("MLP", mlp(kanal, sisi))]:
        n_param = sum(p.numel() for p in model.parameters())
        print(f"{nama}: {n_param} parameter")
        akurasi, durasi = latih_dan_uji(model, latih, uji, a.epoch, perangkat)
        print(f"{nama}: akurasi uji {akurasi:.4f}, waktu latih {durasi:.1f} detik\n")


if __name__ == "__main__":
    main()
