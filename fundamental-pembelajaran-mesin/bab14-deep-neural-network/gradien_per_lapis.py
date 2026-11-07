"""Norma gradien per lapisan pada jaringan 30 lapisan saat inisialisasi:
sigmoid polos, sigmoid dengan residual, dan ReLU polos dengan inisialisasi He.
Data untuk Gambar 11.3 di buku. Kode 11.2 pada buku."""
import torch
from torch import nn

torch.manual_seed(0)
D, LEBAR = 30, 256


class Blok(nn.Module):
    def __init__(self, aktivasi, residual):
        super().__init__()
        self.lin = nn.Linear(LEBAR, LEBAR)
        self.akt = aktivasi
        self.residual = residual
        if isinstance(aktivasi, nn.ReLU):
            nn.init.kaiming_normal_(self.lin.weight, nonlinearity="relu")
        else:
            nn.init.xavier_normal_(self.lin.weight)
        nn.init.zeros_(self.lin.bias)

    def forward(self, x):
        h = self.akt(self.lin(x))
        return x + h if self.residual else h


def norma_gradien(aktivasi, residual):
    model = nn.Sequential(*[Blok(aktivasi, residual) for _ in range(D)], nn.Linear(LEBAR, 10))
    x = torch.randn(512, LEBAR)
    y = torch.randint(0, 10, (512,))
    loss = nn.functional.cross_entropy(model(x), y)
    loss.backward()
    return [model[i].lin.weight.grad.norm().item() for i in range(D)]


for nama, akt, res in [("sigmoid polos", nn.Sigmoid(), False),
                       ("sigmoid + residual", nn.Sigmoid(), True),
                       ("ReLU + He polos", nn.ReLU(), False)]:
    g = norma_gradien(akt, res)
    print(f"{nama:16s}", " ".join(f"({i + 1},{v:.3g})" for i, v in enumerate(g)))
