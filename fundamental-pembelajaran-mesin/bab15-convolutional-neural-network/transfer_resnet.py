"""Kode 12.4 - Transfer learning ResNet-18 untuk klasifikasi citra kecil.

Struktur folder data (format ImageFolder):
    data_daun/latih/<nama_kelas>/*.jpg
    data_daun/uji/<nama_kelas>/*.jpg

Jalankan:
    python transfer_resnet.py --data data_daun --epoch-head 5 --epoch-ft 5
"""
import argparse

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def jalankan_epoch(model, loader, opt, loss_fn, perangkat, latih=True):
    model.train(latih)
    total, benar, jumlah_loss = 0, 0, 0.0
    with torch.set_grad_enabled(latih):
        for x, y in loader:
            x, y = x.to(perangkat), y.to(perangkat)
            keluaran = model(x)
            loss = loss_fn(keluaran, y)
            if latih:
                opt.zero_grad()
                loss.backward()
                opt.step()
            jumlah_loss += loss.item() * len(y)
            benar += (keluaran.argmax(1) == y).sum().item()
            total += len(y)
    return jumlah_loss / total, benar / total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data_daun")
    ap.add_argument("--epoch-head", type=int, default=5)
    ap.add_argument("--epoch-ft", type=int, default=5)
    a = ap.parse_args()
    perangkat = "cuda" if torch.cuda.is_available() else "cpu"

    bobot = models.ResNet18_Weights.DEFAULT
    praproses = bobot.transforms()  # resize, crop, normalisasi ImageNet
    augmentasi = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    latih = datasets.ImageFolder(f"{a.data}/latih", transform=augmentasi)
    uji = datasets.ImageFolder(f"{a.data}/uji", transform=praproses)
    dl_latih = DataLoader(latih, batch_size=32, shuffle=True)
    dl_uji = DataLoader(uji, batch_size=64)
    n_kelas = len(latih.classes)
    print("Kelas:", latih.classes)

    model = models.resnet18(weights=bobot)
    for p in model.parameters():          # 1) bekukan backbone
        p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, n_kelas)
    model = model.to(perangkat)
    loss_fn = nn.CrossEntropyLoss()

    opt = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
    for e in range(a.epoch_head):
        lt, at = jalankan_epoch(model, dl_latih, opt, loss_fn, perangkat, True)
        lu, au = jalankan_epoch(model, dl_uji, None, loss_fn, perangkat, False)
        print(f"[head] epoch {e + 1}: akurasi latih {at:.3f}, akurasi uji {au:.3f}")

    for p in model.layer4.parameters():   # 2) fine-tuning blok terakhir
        p.requires_grad = True
    opt = torch.optim.Adam([
        {"params": model.layer4.parameters(), "lr": 1e-4},
        {"params": model.fc.parameters(), "lr": 1e-3},
    ])
    for e in range(a.epoch_ft):
        lt, at = jalankan_epoch(model, dl_latih, opt, loss_fn, perangkat, True)
        lu, au = jalankan_epoch(model, dl_uji, None, loss_fn, perangkat, False)
        print(f"[fine-tune] epoch {e + 1}: akurasi latih {at:.3f}, akurasi uji {au:.3f}")

    torch.save(model.state_dict(), "resnet18_daun.pt")
    # Ekspor ke ONNX untuk layanan inferensi (Gambar 12.11)
    model.eval().cpu()
    torch.onnx.export(model, torch.randn(1, 3, 224, 224), "resnet18_daun.onnx",
                      input_names=["citra"], output_names=["logit"])
    print("Model disimpan: resnet18_daun.pt dan resnet18_daun.onnx")


if __name__ == "__main__":
    main()
