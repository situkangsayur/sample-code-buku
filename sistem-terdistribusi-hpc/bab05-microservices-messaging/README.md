# Bab 5 - Arsitektur Aplikasi, Microservices, dan Messaging

Contoh kode untuk Bab 5 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Berkas | Isi | Kaitan di buku |
|---|---|---|
| `producer_rabbit.py` | Producer RabbitMQ (durable, persistent, message_id) | Kode 5.1 |
| `consumer_rabbit.py` | Consumer RabbitMQ dengan ack setelah proses, prefetch, nack | Kode 5.2 |
| `docker-compose.yml`, `notifikasi/` | RabbitMQ 4, Kafka 4 mode KRaft, layanan notifikasi | Kode 5.3, 5.5 |
| `kafka_pesanan.py` | Producer ber-key dan consumer group dengan commit manual | Kode 5.4 |
| `consumer_idempoten.py` | Deduplication dalam satu transaksi (SQLite, tanpa broker) | Kode 5.6, Algoritma 5.1 |
| `outbox_relay.py` | Transactional outbox dan relay polling | Kode 5.7, Algoritma 5.2 |
| `saga_orkestrator.py` | Orchestrator saga dengan kompensasi (simulasi) | Algoritma 5.3 |
| `retry_backoff.py` | Retry dengan exponential backoff dan full jitter | Kode 5.8 |
| `breaker/` | Circuit breaker Go (sony/gobreaker) dengan layanan palsu | Kode 5.9 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# tanpa broker
python consumer_idempoten.py
python outbox_relay.py --cetak
python saga_orkestrator.py gagal
python retry_backoff.py
(cd breaker && go run .)

# dengan broker
docker compose up -d rabbitmq kafka
python producer_rabbit.py 1000
python consumer_rabbit.py
python kafka_pesanan.py kirim 20
python kafka_pesanan.py baca notifikasi
python kafka_pesanan.py baca analitik
```

## Praktikum ketahanan (Subbab 5.11)

1. Matikan consumer, kirim 100 pesan (`python producer_rabbit.py 100`), nyalakan lagi. Semua pesan harus terproses.
2. Jalankan `JEDA_SEBELUM_ACK=5 python consumer_rabbit.py`, kirim satu pesan, lalu hentikan
   consumer dengan Ctrl+C sebelum 5 detik. Nyalakan lagi: pesan yang sama dikirim ulang (at-least-once).
3. Jalankan dua consumer sekaligus dan amati pembagian pesan (competing consumers).
4. Kafka: topik dibuat dengan 3 partition (`KAFKA_NUM_PARTITIONS`); baca dengan dua grup berbeda,
   lalu baca ulang dari awal dengan nama grup baru.

Dasbor RabbitMQ: http://localhost:15672 (guest/guest, hanya untuk lokal).
