#!/usr/bin/env bash
# Kode 2.8 dan 2.9: alat mengamati jaringan dan tc netem.
# Pemakaian: ./amati.sh info | tangkap | jelek | pulih
case "${1:-info}" in
  info)
    ss -tulpn                         # siapa mendengar di port mana
    ss -tan state established         # koneksi TCP terbuka
    ss -ti dst 127.0.0.1              # rtt, cwnd, retrans per koneksi
    sysctl net.ipv4.tcp_congestion_control ;;
  tangkap)
    sudo tcpdump -i lo -nn -w echo.pcap 'port 9000 or port 9001' ;;
  jelek)
    sudo tc qdisc add dev lo root netem delay 50ms loss 5%
    tc qdisc show dev lo ;;
  pulih)
    sudo tc qdisc del dev lo root     # WAJIB setelah eksperimen
    tc qdisc show dev lo ;;
  *) echo "pakai: $0 info|tangkap|jelek|pulih" ;;
esac
