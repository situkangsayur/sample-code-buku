# Bab 9 - Spark Skala Besar: HPC Data

Contoh kode lengkap untuk Bab 9 buku *Data Engineering 101*.

| Berkas | Isi | Rujukan di buku |
|---|---|---|
| `gen_data.py` | Pembangkit data sintetis (sama dengan Bab 8) | semua contoh |
| `aqe_join.py` | Konfigurasi AQE; broadcast vs sort-merge, dengan `explain()` dan waktu | Kode 9.2, Tabel 9.2 |
| `salting.py` | Join transaksi dan rekening (dua tabel besar); rekening penampung "berat" 40 persen; join biasa vs bersalting (garam hanya untuk kunci berat) | Kode 9.4 |
| `scala-skala/` | Salting dalam Scala | Kode 9.5 |
| `iceberg_merge.py` | MERGE, dynamic partition overwrite, `rewrite_data_files`, `expire_snapshots` | Kode 9.7-9.8 |
| `submit_k8s.sh` | `spark-submit` ke Kubernetes dengan event log dan dynamic allocation | Kode 9.9 |
| `scaling_bench.py` | Pengukur strong scaling: median, speedup, efisiensi, biaya, CSV | Kode 9.10, Algoritma 9.1 |
| `gold_harian.py` | Job gold yang diukur (sama dengan Bab 8) | Kode 9.10 |
| `baseline_duckdb.py` | Baseline satu mesin DuckDB | Kode 9.11 |
| `baseline-datafusion/` | Baseline satu mesin DataFusion (Rust) | Kode 9.12 |

Nomor Kode dapat bergeser sedikit bila isi buku berubah; cocokkan dengan judul listing.

## Menjalankan

```bash
pip install -r requirements.txt               # Java 17 untuk PySpark
python gen_data.py --baris 5000000 --keluar data
spark-submit aqe_join.py data
spark-submit salting.py 5000000
spark-submit --packages org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1 iceberg_merge.py data
python scaling_bench.py --master "local[{core}]" --data data --core 1 2 4
python baseline_duckdb.py data
cd baseline-datafusion && cargo run --release -- ../data
cd scala-skala && sbt package && spark-submit --class Salting target/scala-2.12/skala_2.12-0.1.jar
```

Untuk weak scaling, bangkitkan data sebanding jumlah core (misalnya `--baris 5000000` per core)
dan jalankan `scaling_bench.py` sekali per ukuran data.

Catatan: di satu laptop semua worker berbagi CPU, memori, dan disk. Jangan memakai jumlah core
melebihi core fisik, dan tuliskan batas ini saat melaporkan hasil.
