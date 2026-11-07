#!/usr/bin/env bash
# Perintah HDFS yang dibahas di Bab 3 (Kode 3.x). Jalankan di mesin yang punya klien Hadoop.
set -euo pipefail
hdfs dfs -mkdir -p /lake/bronze/transaksi/tanggal=2026-10-19
hdfs dfs -put part-0000.parquet /lake/bronze/transaksi/tanggal=2026-10-19/
# Lihat blok, replika, dan lokasinya
hdfs fsck /lake/bronze/transaksi -files -blocks -locations
# Ringkasan kapasitas dan DataNode yang hidup atau mati
hdfs dfsadmin -report | head -40
# Erasure coding untuk data dingin: aktifkan kebijakan lalu pasang di direktori
hdfs ec -listPolicies
hdfs ec -enablePolicy -policy RS-6-3-1024k
hdfs dfs -mkdir -p /lake/cold
hdfs ec -setPolicy -path /lake/cold -policy RS-6-3-1024k
hdfs ec -getPolicy -path /lake/cold
