#!/usr/bin/env bash
# Kode 3.5: menguraikan waktu muat per versi HTTP dengan curl -w, diulang N kali.
# Pemakaian: ./ukur_versi.sh https://www.cloudflare.com/ 10
URL=${1:-https://www.cloudflare.com/}
N=${2:-10}
FMT='dns=%{time_namelookup} tcp=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total} versi=%{http_version}\n'
for v in --http1.1 --http2 --http3; do
  echo "== $v"
  for _ in $(seq "$N"); do
    curl -so /dev/null -w "$FMT" "$v" "$URL" 2>/dev/null || { echo "(curl tidak mendukung $v)"; break; }
  done
done
echo "== iklan HTTP/3"
curl -sI --http2 "$URL" | grep -i alt-svc
