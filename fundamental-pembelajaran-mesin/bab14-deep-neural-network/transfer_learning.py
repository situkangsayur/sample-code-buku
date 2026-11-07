"""Transfer learning dengan ResNet-18 terlatih ImageNet (torchvision) pada CIFAR-10:
mode 'fitur' (backbone dibekukan) dan mode 'finetune' (semua lapisan, lr berbeda).
Kode 11.5 pada buku. Jalankan: python transfer_learning.py --mode fitur --n-latih 5000"""
import argparse

import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, models


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["fitur", "finetune"], default="fitur")
    ap.add_argument("--n-latih", type=int, default=5000)   # sengaja sedikit data
    ap.add_argument("--epoch", type=int, default=3)
    a = ap.parse_args()
    torch.manual_seed(0)
    dev = "cuda" if torch.cuda.is_available() else "cpu"

    bobot = models.ResNet18_Weights.IMAGENET1K_V1
    tf = bobot.transforms()                         # praproses yang sama dengan saat pretraining
    latih = datasets.CIFAR10("data", train=True, download=True, transform=tf)
    uji = datasets.CIFAR10("data", train=False, download=True, transform=tf)
    latih = Subset(latih, torch.randperm(len(latih))[: a.n_latih].tolist())
    uji = Subset(uji, list(range(2000)))
    dl, dl_uji = DataLoader(latih, 64, shuffle=True), DataLoader(uji, 256)

    model = models.resnet18(weights=bobot)
    model.fc = nn.Linear(model.fc.in_features, 10)  # kepala baru untuk 10 kelas
    beku = a.mode == "fitur"
    if beku:
        for nama, p in model.named_parameters():
            p.requires_grad = nama.startswith("fc.")  # hanya kepala yang dilatih
        opt = torch.optim.AdamW(model.fc.parameters(), lr=1e-3)
    else:
        badan = [p for n, p in model.named_parameters() if not n.startswith("fc.")]
        opt = torch.optim.AdamW([{"params": badan, "lr": 1e-4},          # lr kecil untuk backbone
                                 {"params": model.fc.parameters(), "lr": 1e-3}])
    model.to(dev)

    for epoch in range(a.epoch):
        model.train()
        if beku:
            model.eval()                            # BN backbone memakai statistik ImageNet
        for xb, yb in dl:
            loss = nn.functional.cross_entropy(model(xb.to(dev)), yb.to(dev))
            opt.zero_grad(); loss.backward(); opt.step()
        model.eval()
        with torch.no_grad():
            benar = sum((model(xb.to(dev)).argmax(1).cpu() == yb).sum().item() for xb, yb in dl_uji)
        print(f"mode={a.mode} epoch {epoch + 1}: akurasi uji {benar / len(uji):.3f}")


if __name__ == "__main__":
    main()
