#!/usr/bin/env bash
# Kebijakan per peran di RustFS dan uji penolakan (Kode 13.9).
# Prasyarat: klien `rc` dari proyek RustFS (https://github.com/rustfs/cli) dan alias admin
# 'lab' yang sudah dibuat dengan: rc alias set lab "$S3_ENDPOINT" "$S3_ACCESS_KEY" "$S3_SECRET_KEY"
# Sintaks `rc admin` dapat berubah antarversi; periksa `rc admin policy --help`.
set -u
: "${ANI_PASSWORD:?isi ANI_PASSWORD dari .env atau secret manager}"
S3_ENDPOINT=${S3_ENDPOINT:-https://rustfs:9000}

cat > analis.json <<'JSON'
{"Version": "2012-10-17",
 "Statement": [{"Effect": "Allow",
   "Action": ["s3:GetObject", "s3:ListBucket"],
   "Resource": ["arn:aws:s3:::silver", "arn:aws:s3:::silver/*",
                "arn:aws:s3:::gold",   "arn:aws:s3:::gold/*"]}]}
JSON
rc admin policy create lab/ analis analis.json
rc admin user add lab/ ani "$ANI_PASSWORD"
rc admin policy attach lab/ analis --user ani

rc alias set lab-ani "$S3_ENDPOINT" ani "$ANI_PASSWORD"
if rc cp lab-ani/bronze/nasabah.parquet /tmp/uji-bronze.parquet 2>/dev/null; then
  echo "GAGAL: analis dapat membaca bronze"; exit 1
else
  echo "OK: akses bronze ditolak (cari entrinya di audit log RustFS)"
fi
