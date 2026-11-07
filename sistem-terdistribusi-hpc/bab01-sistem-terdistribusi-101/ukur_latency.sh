#!/usr/bin/env bash
# Kode 1.5: mengukur latency ke tiga benua dengan ping, traceroute, dan curl.
set -u
SITUS=("www.tazkia.ac.id" "www.nus.edu.sg" "www.tudelft.nl")
for s in "${SITUS[@]}"; do
  echo "== $s"
  ping -c 10 "$s" | tail -1                     # ringkasan min/avg/max RTT
  curl -so /dev/null -w "dns=%{time_namelookup} tcp=%{time_connect} tls=%{time_appconnect} total=%{time_total}\n" "https://$s/"
done
echo "== traceroute ke Eropa"
traceroute -q 1 www.tudelft.nl || echo "traceroute belum terpasang"
