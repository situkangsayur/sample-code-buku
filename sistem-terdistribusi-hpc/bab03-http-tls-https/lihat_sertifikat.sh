#!/usr/bin/env bash
# Kode 3.6: melihat handshake TLS dan rantai sertifikat.
H=${1:-www.google.com}
openssl s_client -connect "$H:443" -servername "$H" </dev/null 2>/dev/null | sed -n '/Certificate chain/,/---/p'
openssl s_client -connect "$H:443" -servername "$H" </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
curl -vI "https://$H" 2>&1 | grep -E "SSL connection|subject|issuer"
