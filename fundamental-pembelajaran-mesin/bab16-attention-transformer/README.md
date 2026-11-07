# Bab 13 - Attention dan Transformer

Kode pendamping buku *Fundamental Pembelajaran Mesin* (Hendri Karisma), Bab 13.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `self_attention_numpy.py` | Dot-product attention, self-attention (dengan/tanpa causal mask dan penskalaan), uji permutation equivariance, positional encoding; memeriksa semua contoh hitungan bab | Kode 13.1 |
| `mha_pytorch.py` | `nn.MultiheadAttention`, jumlah parameter, causal mask, dan pengukuran biaya terhadap panjang urutan | Kode 13.2 |
| `blok_transformer.py` | Satu blok encoder Pre-LN, positional encoding sinusoidal, perbandingan dengan `nn.TransformerEncoderLayer` | Kode 13.3 |
| `attention-rust/` | Scaled dot-product attention dalam Rust tanpa crate | Kode 13.4 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python self_attention_numpy.py
python mha_pytorch.py
python blok_transformer.py

cd attention-rust && cargo run --release
```
