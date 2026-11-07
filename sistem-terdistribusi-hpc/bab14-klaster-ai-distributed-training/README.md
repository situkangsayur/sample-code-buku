# Bab 14 - Klaster AI dan Distributed Training

Contoh kode untuk Bab 14 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `hitung.py` | Kalkulator memori ZeRO, waktu 6ND, bubble pipeline, MTBF, selang checkpoint, energi, biaya | Subbab memori, waktu, keandalan, biaya |
| `param_server.py` | Parameter server sinkron dan asinkron dengan Ray actor | Kode 14.1 |
| `ring_allreduce.py` | Simulasi ring all-reduce (reduce-scatter + all-gather) dan jumlah byte terkirim | Algoritma 14.1 |
| `ddp_latih.py` | PyTorch DDP, `torchrun`, `DistributedSampler`, checkpoint per epoch dan restart | Kode 14.2, 14.3, 14.4 |
| `amp_latih.py` | Mixed precision: `autocast` BF16/FP16 dan `GradScaler` | Kode 14.5 |
| `fsdp_latih.py` | FSDP dengan BF16 dan sharded checkpoint (`torch.distributed.checkpoint`) | Kode 14.6 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python ring_allreduce.py --peserta 8          # tanpa GPU
python hitung.py --param 70e9 --gpu 64        # semua angka masukan adalah asumsi
python param_server.py --mode sinkron && python param_server.py --mode asinkron

python ddp_latih.py --sintetis                # satu proses (acuan)
torchrun --nproc_per_node=2 ddp_latih.py --sintetis --thread 2   # CPU + gloo
torchrun --nproc_per_node=2 ddp_latih.py      # 2 GPU + NCCL (Kaggle T4 x2)
# uji kegagalan: hentikan dengan Ctrl+C di tengah, lalu jalankan lagi -> lanjut dari ckpt.pt

python amp_latih.py --dtype bf16              # butuh GPU; BF16 butuh GPU Ampere ke atas
torchrun --nproc_per_node=2 fsdp_latih.py     # butuh >= 2 GPU
```

Dua mesin, masing-masing 4 GPU (jalankan di setiap mesin):

```bash
torchrun --nnodes=2 --nproc_per_node=4 --rdzv_backend=c10d \
  --rdzv_endpoint=10.0.0.1:29500 ddp_latih.py
```
