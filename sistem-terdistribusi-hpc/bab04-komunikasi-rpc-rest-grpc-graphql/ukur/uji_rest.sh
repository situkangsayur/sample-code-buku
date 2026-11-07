#!/usr/bin/env bash
# Uji beban REST dengan k6 pada 10, 50, dan 200 VU, masing-masing tiga kali.
# Jalankan server dulu: (cd go-katalog && go run ./rest)
set -euo pipefail
cd "$(dirname "$0")"
URL=${URL:-http://localhost:8080}
for v in 10 50 200; do
  for ulang in 1 2 3; do
    echo "== vus=$v ulangan=$ulang"
    k6 run --quiet -e URL="$URL" -e VUS="$v" -e DURASI=20s uji_rest.js \
      | grep -E 'http_req_duration|http_reqs|checks' || true
  done
done
