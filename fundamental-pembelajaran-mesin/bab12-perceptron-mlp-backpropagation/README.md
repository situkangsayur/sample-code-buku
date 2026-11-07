# Bab 9 - Perceptron, Multilayer Perceptron, dan Backpropagation

Kode pendamping buku *Fundamental Pembelajaran Mesin* (Hendri Karisma), Bab 9.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `perceptron_numpy.py` | Aturan belajar perceptron pada AND, OR, XOR | Kode 9.1 |
| `perceptron_rust/` | Perceptron dalam Rust tanpa crate | Kode 9.2 |
| `backprop_manual.py` | Contoh hitung satu iterasi backpropagation 2-2-1 + gradient checking | Kode 9.3 |
| `backprop_torch.py` | Contoh hitung yang sama dengan autograd PyTorch | Kode 9.4 |
| `mlp_xor_numpy.py` | MLP 2-4-1 dari nol untuk XOR | Kode 9.5 |
| `mlp_torch_mnist.py` | MLP 784-256-128-10 PyTorch untuk MNIST (unduh otomatis ke `data/`) | Kode 9.6 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python perceptron_numpy.py
python backprop_manual.py
python backprop_torch.py
python mlp_xor_numpy.py
python mlp_torch_mnist.py      # sekitar 97-98% akurasi uji setelah 5 epoch

cd perceptron_rust && cargo run --release
```
