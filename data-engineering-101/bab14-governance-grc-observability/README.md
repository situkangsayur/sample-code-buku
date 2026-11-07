# Bab 14 - Data governance, GRC, dan observability

Contoh kode Bab 14 buku *Data Engineering 101* (data sintetis).

| Berkas | Isi | Kode di buku |
|---|---|---|
| `openlineage_event.py` | mengirim event OpenLineage ke Marquez | Kode 14.1 |
| `contract.yaml` | contoh data contract | Kode 14.2 |
| `validasi_contract.py` | validasi batch terhadap kontrak (Polars) | Kode 14.3 |
| `hapus_nasabah.sql` | hapus satu nasabah di Iceberg + expire snapshot | Kode 14.4 |
| `obs/cek_tabel.py`, `obs/volume.sql` | pemeriksaan freshness dan volume (seasonal z-score) | Kode 14.5 |
| `obs/demo_lokal.py` | demo lokal pemeriksaan volume tanpa Iceberg | - |
| `runbook.yaml` | runbook "silver.transaksi terlambat" | Kode 14.6 |
| `risk_register.py` | skor inheren/residual vs risk appetite | Tabel 14.3 |
| `error_budget.py` | error budget dan jejak energi | contoh di subbab 14.7-14.8 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python validasi_contract.py     # sengaja gagal: contoh berisi pelanggaran
python obs/demo_lokal.py        # memicu peringatan volume
python risk_register.py
python error_budget.py
# Marquez (penerima OpenLineage): ikuti petunjuk di https://github.com/MarquezProject/marquez
python openlineage_event.py
```

`hapus_nasabah.sql` dijalankan di Spark SQL dengan katalog Iceberg `lake`.
Nomor Kode mengikuti urutan di bab; periksa kembali bila bab disunting.
