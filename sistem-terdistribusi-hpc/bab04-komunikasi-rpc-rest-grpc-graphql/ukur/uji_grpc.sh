#!/usr/bin/env bash
# Uji beban gRPC dengan ghz (https://ghz.sh) pada 10, 50, dan 200 pemanggil
# serentak, masing-masing tiga kali. Keluaran ringkas: P50, P99, RPS.
# Jalankan server dulu: (cd go-katalog && go run ./grpcserver)
set -euo pipefail
cd "$(dirname "$0")/.."
PROTO=go-katalog/proto/katalog/v1/katalog.proto
for c in 10 50 200; do
  for ulang in 1 2 3; do
    echo "== c=$c ulangan=$ulang"
    ghz --insecure --proto "$PROTO" --import-paths go-katalog/proto \
        --call katalog.v1.Katalog.AmbilProduk \
        -d '{"id": 42}' -m '{"authorization":"Bearer rahasia"}' \
        -c "$c" -n 20000 localhost:50051 \
      | grep -E 'Requests/sec|50 % in|99 % in|Error distribution' || true
  done
done
