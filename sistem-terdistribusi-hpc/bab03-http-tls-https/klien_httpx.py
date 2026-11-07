"""Kode 3.3: klien HTTP/2 dengan httpx.

Pasang: pip install -r requirements.txt   Jalankan: python3 klien_httpx.py
"""
import httpx

batas = httpx.Timeout(5.0, connect=2.0)  # selalu pasang timeout
with httpx.Client(http2=True, timeout=batas) as klien:
    for jalur in ["/", "/about/", "/blog/"]:  # satu koneksi dipakai ulang
        r = klien.get("https://www.cloudflare.com" + jalur)
        print(r.http_version, r.status_code, len(r.content), "byte",
              r.headers.get("alt-svc", "-")[:30])
