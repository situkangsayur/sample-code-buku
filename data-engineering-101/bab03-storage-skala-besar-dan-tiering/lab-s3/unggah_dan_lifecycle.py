"""Unggah data berpartisi tanggal ke object storage S3-compatible dan pasang lifecycle rule (Kode 3.x).

Prasyarat: docker compose up -d di folder ini, lalu
    export S3_ACCESS_KEY=... S3_SECRET_KEY=...   (sama dengan .env)
    export S3_ENDPOINT=http://localhost:9000      (opsional)
"""
import os
import sys

import boto3
import polars as pl

sys.path.insert(0, "..")
from bangkit_data import bangkit  # noqa: E402

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("S3_ENDPOINT", "http://localhost:9000"),
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
)
BUCKET = "bank-lake"
if BUCKET not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
    s3.create_bucket(Bucket=BUCKET)

# Satu berkas Parquet per tanggal, mengikuti partisi gaya Hive: tanggal=YYYY-MM-DD
df = bangkit(300_000).with_columns(pl.col("waktu").dt.date().alias("tanggal"))
os.makedirs("tmp", exist_ok=True)
for (tgl,), bagian in df.filter(pl.col("tanggal") < pl.date(2026, 2, 1)).group_by("tanggal"):
    lokal = f"tmp/{tgl}.parquet"
    bagian.drop("tanggal").write_parquet(lokal, compression="zstd")
    s3.upload_file(lokal, BUCKET, f"bronze/transaksi/tanggal={tgl}/part-0000.parquet")
print("terunggah:", s3.list_objects_v2(Bucket=BUCKET, Prefix="bronze/")["KeyCount"], "objek")

# Lifecycle: hapus data bronze transaksi setelah kira-kira 10 tahun.
# Transisi ke kelas lain memerlukan tier tujuan; di S3 sungguhan lihat lifecycle_s3.json.
s3.put_bucket_lifecycle_configuration(
    Bucket=BUCKET,
    LifecycleConfiguration={"Rules": [{
        "ID": "transaksi-retensi",
        "Filter": {"Prefix": "bronze/transaksi/"},
        "Status": "Enabled",
        "Expiration": {"Days": 3653},
    }]},
)
print(s3.get_bucket_lifecycle_configuration(Bucket=BUCKET)["Rules"])
