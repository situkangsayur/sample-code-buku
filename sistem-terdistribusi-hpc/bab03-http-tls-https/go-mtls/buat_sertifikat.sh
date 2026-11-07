#!/usr/bin/env bash
# Membuat CA internal, sertifikat server (localhost), dan sertifikat klien untuk uji mTLS.
set -euo pipefail
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes -days 30 \
  -keyout ca-key.pem -out ca.pem -subj "/CN=CA Internal Contoh"
buat() { # $1 = nama berkas, $2 = CN, $3 = extfile
  openssl req -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes \
    -keyout "$1-key.pem" -out "$1.csr" -subj "/CN=$2"
  openssl x509 -req -in "$1.csr" -CA ca.pem -CAkey ca-key.pem -CAcreateserial \
    -days 30 -out "$1.pem" -extfile <(printf "%s" "$3")
  rm "$1.csr"
}
buat server localhost "subjectAltName=DNS:localhost,IP:127.0.0.1
extendedKeyUsage=serverAuth"
buat klien layanan-pesanan "extendedKeyUsage=clientAuth"
echo "selesai: ca.pem server.pem klien.pem"
