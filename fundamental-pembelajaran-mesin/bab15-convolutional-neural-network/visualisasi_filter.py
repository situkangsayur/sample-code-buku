"""Kode 12.5 - Visualisasi filter lapis pertama dan feature map ResNet-18.

Jalankan:
    python visualisasi_filter.py                 # hanya filter
    python visualisasi_filter.py --citra daun.jpg  # filter + feature map
"""
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision import models


def simpan_filter(model, berkas="filter_resnet18.png"):
    w = model.conv1.weight.detach()          # (64, 3, 7, 7)
    w = (w - w.min()) / (w.max() - w.min())  # skala ke [0, 1]
    fig, axes = plt.subplots(8, 8, figsize=(6, 6))
    for i, ax in enumerate(axes.flat):
        ax.imshow(w[i].permute(1, 2, 0))     # CHW -> HWC
        ax.axis("off")
    fig.savefig(berkas, dpi=150)
    print("Disimpan:", berkas)


def simpan_feature_map(model, praproses, path_citra):
    hasil = {}

    def hook(nama):
        def f(modul, masukan, keluaran):
            hasil[nama] = keluaran.detach()
        return f

    model.layer1.register_forward_hook(hook("layer1"))
    model.layer4.register_forward_hook(hook("layer4"))
    x = praproses(Image.open(path_citra).convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        prob = model(x).softmax(1)
    print("Kelas ImageNet teratas (indeks):", prob.topk(3).indices.tolist())

    for nama, peta in hasil.items():
        fig, axes = plt.subplots(4, 8, figsize=(8, 4))
        for i, ax in enumerate(axes.flat):
            ax.imshow(peta[0, i], cmap="viridis")
            ax.axis("off")
        fig.suptitle(f"feature map {nama}, bentuk {tuple(peta.shape[1:])}")
        fig.savefig(f"fmap_{nama}.png", dpi=120)
        print("Disimpan:", f"fmap_{nama}.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--citra", default=None)
    a = ap.parse_args()
    bobot = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=bobot).eval()
    simpan_filter(model)
    if a.citra:
        simpan_feature_map(model, bobot.transforms(), a.citra)


if __name__ == "__main__":
    main()
