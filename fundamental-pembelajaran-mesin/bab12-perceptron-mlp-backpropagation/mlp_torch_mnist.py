"""MLP 784-256-128-10 dengan PyTorch pada MNIST. Kode 9.6 pada buku."""
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

torch.manual_seed(0)
perangkat = "cuda" if torch.cuda.is_available() else "cpu"

tf = transforms.Compose([transforms.ToTensor(),
                         transforms.Normalize((0.1307,), (0.3081,))])
latih = datasets.MNIST("data", train=True, download=True, transform=tf)
uji = datasets.MNIST("data", train=False, download=True, transform=tf)
dl_latih = DataLoader(latih, batch_size=128, shuffle=True)
dl_uji = DataLoader(uji, batch_size=1000)

model = nn.Sequential(
    nn.Flatten(),                       # 28x28 -> 784
    nn.Linear(784, 256), nn.ReLU(),
    nn.Linear(256, 128), nn.ReLU(),
    nn.Linear(128, 10),                 # logit 10 kelas (tanpa softmax)
).to(perangkat)
loss_fn = nn.CrossEntropyLoss()         # softmax + cross-entropy sekaligus
opt = torch.optim.SGD(model.parameters(), lr=0.1)

for epoch in range(5):
    model.train()
    for xb, yb in dl_latih:
        xb, yb = xb.to(perangkat), yb.to(perangkat)
        loss = loss_fn(model(xb), yb)   # forward
        opt.zero_grad()
        loss.backward()                 # backpropagation
        opt.step()                      # gradient descent
    model.eval()
    benar = 0
    with torch.no_grad():
        for xb, yb in dl_uji:
            pred = model(xb.to(perangkat)).argmax(1)
            benar += (pred == yb.to(perangkat)).sum().item()
    print(f"epoch {epoch + 1}: akurasi uji {benar / len(uji):.4f}")
