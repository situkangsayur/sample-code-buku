#!/usr/bin/env bash
# Kode 8.3: eksperimen strong scaling (pemanasan + 5 ulangan per p).
set -euo pipefail
go build -o prima prima.go
rm -f hasil.csv
./prima 1 > /dev/null                 # pemanasan, dibuang
for p in 1 2 4 8 $(nproc); do
  for r in 1 2 3 4 5; do ./prima "$p" >> hasil.csv; done
done
python3 olah.py hasil.csv
