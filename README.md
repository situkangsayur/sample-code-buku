# Contoh kode buku ajar STMIK Tazkia

Kode lengkap untuk tiga buku ajar Teknik Informatika STMIK Tazkia karya Hendri Karisma. Setiap
folder `babNN-*` berisi kode yang dirujuk lewat baris "Kode lengkap:" di buku, README per bab,
dan `requirements.txt` atau `docker-compose.yml` bila perlu.

| Folder | Buku |
|---|---|
| [`sistem-terdistribusi-hpc/`](sistem-terdistribusi-hpc/) | *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi* (14 bab) |
| [`data-engineering-101/`](data-engineering-101/) | *Data Engineering 101* (14 bab) |
| [`fundamental-pembelajaran-mesin/`](fundamental-pembelajaran-mesin/) | *Fundamental Pembelajaran Mesin*, bersama Hairul Umam (17 bab) |

File `.env.example`/`.env.contoh` hanya berisi nilai contoh. Salin menjadi `.env` dan ganti
nilainya sebelum menjalankan `docker compose`.
