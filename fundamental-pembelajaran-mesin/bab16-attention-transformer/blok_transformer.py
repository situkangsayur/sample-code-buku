"""Kode 13.3 - Satu blok encoder transformer (Pre-LN) dan positional encoding sinusoidal.

Juga membandingkan jumlah parameternya dengan nn.TransformerEncoderLayer.
"""
import math

import torch
from torch import nn


class BlokEncoder(nn.Module):
    def __init__(self, d=512, h=8, d_ff=2048, p=0.1):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        self.ffn = nn.Sequential(nn.Linear(d, d_ff), nn.GELU(),
                                 nn.Linear(d_ff, d), nn.Dropout(p))

    def forward(self, x, pad_mask=None):
        a = self.ln1(x)
        x = x + self.attn(a, a, a, key_padding_mask=pad_mask)[0]
        return x + self.ffn(self.ln2(x))


def positional_encoding(n, d):
    pos = torch.arange(n).unsqueeze(1)
    div = torch.exp(torch.arange(0, d, 2) * (-math.log(10000.0) / d))
    pe = torch.zeros(n, d)
    pe[:, 0::2], pe[:, 1::2] = torch.sin(pos * div), torch.cos(pos * div)
    return pe


if __name__ == "__main__":
    torch.manual_seed(0)
    x = torch.randn(2, 10, 512) + positional_encoding(10, 512)
    blok = BlokEncoder()
    print("keluaran:", blok(x).shape)
    print("parameter BlokEncoder:", sum(p.numel() for p in blok.parameters()))
    resmi = nn.TransformerEncoderLayer(512, 8, 2048, batch_first=True, norm_first=True,
                                       activation="gelu")
    print("parameter nn.TransformerEncoderLayer:", sum(p.numel() for p in resmi.parameters()))

    # padding mask: token terakhir kalimat kedua adalah padding
    pad = torch.zeros(2, 10, dtype=torch.bool)
    pad[1, -1] = True
    print("dengan padding mask:", blok(x, pad).shape)
