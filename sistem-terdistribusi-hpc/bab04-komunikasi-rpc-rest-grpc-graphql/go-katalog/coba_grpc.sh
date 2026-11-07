#!/usr/bin/env bash
# Memanggil gRPC dari terminal dan memeriksa evolusi kontrak.
# Butuh: grpcurl (github.com/fullstorydev/grpcurl) dan buf (buf.build).
# Jalankan server dulu di terminal lain: go run ./grpcserver
set -euo pipefail
cd "$(dirname "$0")"

echo "== daftar layanan (butuh reflection)"
grpcurl -plaintext localhost:50051 list

echo "== unary AmbilProduk"
grpcurl -plaintext -H 'authorization: Bearer rahasia' \
    -d '{"id": 42}' localhost:50051 katalog.v1.Katalog/AmbilProduk

echo "== tanpa token: harus UNAUTHENTICATED"
grpcurl -plaintext -d '{"id": 42}' localhost:50051 katalog.v1.Katalog/AmbilProduk || true

echo "== health check baku"
grpcurl -plaintext -d '{"service": "katalog.v1.Katalog"}' \
    localhost:50051 grpc.health.v1.Health/Check

echo "== server streaming selama 3 detik"
timeout 3 grpcurl -plaintext -H 'authorization: Bearer rahasia' \
    -d '{"id": 42}' localhost:50051 katalog.v1.Katalog/PantauHarga || true

echo "== lint dan breaking check kontrak"
buf lint                                                  # gaya penamaan, struktur
if git rev-parse --verify -q main >/dev/null; then
    # gagalkan CI bila merusak; subdir menunjuk lokasi modul di dalam repo
    buf breaking --against "$(git rev-parse --show-toplevel)/.git#branch=main,subdir=$(git rev-parse --show-prefix)"
else
    echo "(lewati buf breaking: branch main tidak ada)"
fi
