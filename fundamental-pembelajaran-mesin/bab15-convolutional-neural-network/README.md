# Bab 12 - Convolutional Neural Network

Kode pendamping buku *Fundamental Pembelajaran Mesin* (Hendri Karisma), Bab 12.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `konvolusi_numpy.py` | Konvolusi 2D, ReLU, dan max pooling dari nol; memeriksa semua contoh hitungan bab | Kode 12.1 |
| `cnn_mnist.py` | CNN bergaya LeNet-5 dan MLP pembanding, dilatih pada MNIST atau CIFAR-10 | Kode 12.2, 12.3 |
| `transfer_resnet.py` | Transfer learning ResNet-18 (feature extraction lalu fine-tuning) dan ekspor ONNX | Kode 12.4 |
| `visualisasi_filter.py` | Menampilkan filter lapis pertama dan feature map (forward hook) | Kode 12.5 |
| `konvolusi-rust/` | Konvolusi 2D satu kanal dalam Rust tanpa crate | Kode 12.6 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python konvolusi_numpy.py                 # tanpa GPU, tanpa unduhan
python cnn_mnist.py                       # mengunduh MNIST ke ./data
python cnn_mnist.py --data cifar10
python transfer_resnet.py --data data_daun  # siapkan folder ImageFolder sendiri
python visualisasi_filter.py --citra contoh.jpg

cd konvolusi-rust && cargo run --release
```

Untuk `transfer_resnet.py`, susun data dengan pola `data_daun/latih/<kelas>/*.jpg` dan
`data_daun/uji/<kelas>/*.jpg`. Bagi data per tanaman atau per lahan, bukan per foto, agar tidak
terjadi kebocoran data.
