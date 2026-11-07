"""Eksperimen pendukung Bab 10 pada Fashion-MNIST, tanpa torchvision.
  python eksperimen_fashion_mlp.py pembuka 6 10   # skenario pembuka bab: MLP 6 lapisan x 256, 10 epoch
  python eksperimen_fashion_mlp.py tabel          # Tabel 10.x: E01-E03, tiga seed, early stopping
Data diunduh sekali ke folder data_fmnist/. Butuh GPU CUDA (ganti dev = "cpu" bila tidak ada)."""
import gzip, os, sys, time, urllib.request, numpy as np, torch
from torch import nn

D = "data_fmnist"
URL = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"
os.makedirs(D, exist_ok=True)
for f in ("train-images-idx3-ubyte", "train-labels-idx1-ubyte"):
    if not os.path.exists(f"{D}/{f}.gz"):
        urllib.request.urlretrieve(URL + f + ".gz", f"{D}/{f}.gz")
def baca(f, off):
    with gzip.open(f"{D}/{f}.gz") as g:
        return np.frombuffer(g.read(), np.uint8, offset=off)
Xtr = baca("train-images-idx3-ubyte", 16).reshape(-1, 784).astype(np.float32) / 255
ytr = baca("train-labels-idx1-ubyte", 8).astype(np.int64)
dev = "cuda"
Xtr = (Xtr - 0.2860) / 0.3530
X = torch.tensor(Xtr, device=dev); Y = torch.tensor(ytr, device=dev)
idx = torch.randperm(60000, generator=torch.Generator().manual_seed(0)).to(dev)
Xl, Yl, Xv, Yv = X[idx[:55000]], Y[idx[:55000]], X[idx[55000:]], Y[idx[55000:]]

def mlp(dalam, lebar, bn=False, p=0.0):
    lap, n = [], 784
    for _ in range(dalam):
        lap += [nn.Linear(n, lebar)] + ([nn.BatchNorm1d(lebar)] if bn else []) + [nn.ReLU()] + ([nn.Dropout(p)] if p else [])
        n = lebar
    return nn.Sequential(*lap, nn.Linear(n, 10))

def init(model, skema):
    for m in model.modules():
        if isinstance(m, nn.Linear):
            if skema == "he": nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
            elif skema == "kecil": nn.init.normal_(m.weight, 0, 0.01)
            nn.init.zeros_(m.bias)

def evaluasi(model):
    model.eval()
    with torch.no_grad():
        out = model(Xv); l = nn.functional.cross_entropy(out, Yv).item()
        a = (out.argmax(1) == Yv).float().mean().item()
    return l, a

def latih(model, opt, n_epoch, batch=128, seed=0, sabar=None, cetak=True):
    g = torch.Generator(device=dev).manual_seed(seed)
    t0 = time.time(); terbaik = (float("inf"), 0, 0); s = 0; riwayat = []
    for ep in range(1, n_epoch + 1):
        model.train(); perm = torch.randperm(55000, device=dev, generator=g); tot = 0.0
        for i in range(0, 55000, batch):
            j = perm[i:i + batch]
            loss = nn.functional.cross_entropy(model(Xl[j]), Yl[j])
            opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item() * len(j)
        lv, av = evaluasi(model); riwayat.append((ep, tot / 55000, lv, av))
        if cetak: print(f"  ep {ep:2d} latih {tot/55000:.4f} val {lv:.4f} akurasi {av:.4f} ({time.time()-t0:.0f} s)", flush=True)
        if lv < terbaik[0] - 1e-4: terbaik = (lv, av, ep); s = 0
        else:
            s += 1
            if sabar and s >= sabar: break
    return terbaik, riwayat, time.time() - t0

mode = sys.argv[1]
if mode == "pembuka":
    for nama, skema, optf in [("A: He + AdamW 1e-3", "he", lambda p: torch.optim.AdamW(p, lr=1e-3)),
                              ("B: N(0,0.01) + SGD 0.01", "kecil", lambda p: torch.optim.SGD(p, lr=0.01)),
                              ("B2: N(0,0.01) + SGD 0.5", "kecil", lambda p: torch.optim.SGD(p, lr=0.5)),
                              ("B3: default + SGD 1.0", "default", lambda p: torch.optim.SGD(p, lr=1.0)),
                              ]:
        torch.manual_seed(0); m = mlp(int(sys.argv[2]), 256).to(dev); init(m, skema)
        print(nama, flush=True); print(latih(m, optf(m.parameters()), int(sys.argv[3]))[0])
elif mode == "tabel":
    konf = {"E01": (False, 0.0, "sgd"), "E02": (False, 0.0, "adamw"), "E03": (True, 0.3, "adamw")}
    for k, (bn, p, o) in konf.items():
        hasil = []
        for seed in (0, 1, 2):
            torch.manual_seed(seed); m = mlp(2, 512, bn, p).to(dev); init(m, "he")
            opt = torch.optim.SGD(m.parameters(), lr=0.1) if o == "sgd" else torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1e-4)
            (lv, av, ep), _, t = latih(m, opt, 30, seed=seed, sabar=5, cetak=False)
            hasil.append((av, ep)); print(k, seed, f"val loss {lv:.4f} akurasi {av:.4f} epoch {ep} ({t:.0f} s)", flush=True)
        a = np.array([h[0] for h in hasil]) * 100
        print(k, f"{a.mean():.2f} +- {a.std(ddof=1):.2f}", [h[1] for h in hasil], flush=True)
