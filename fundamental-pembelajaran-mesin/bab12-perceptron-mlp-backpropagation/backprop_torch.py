"""Contoh hitung yang sama dengan backprop_manual.py, tetapi gradien dihitung
otomatis oleh autograd PyTorch. Kode 9.4 pada buku."""
import torch

x = torch.tensor([1.0, 1.0]); y = torch.tensor(0.0)
W = torch.tensor([[0.2, -0.3], [0.4, 0.1]], requires_grad=True)
b = torch.tensor([0.1, -0.2], requires_grad=True)
v = torch.tensor([0.5, -0.6], requires_grad=True)
c = torch.tensor(0.3, requires_grad=True)

h = torch.sigmoid(W @ x + b)          # forward: graf komputasi dicatat
y_hat = torch.sigmoid(v @ h + c)
L = 0.5 * (y_hat - y) ** 2
L.backward()                          # backward: aturan rantai otomatis

print("L  =", round(L.item(), 4))
print("dW =", W.grad)
print("db =", b.grad)
print("dv =", v.grad, " dc =", round(c.grad.item(), 4))
