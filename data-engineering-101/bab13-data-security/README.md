# Bab 13 - Data security

Contoh kode Bab 13 buku *Data Engineering 101*. Semua data pribadi di sini sintetis.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `kafka_tls_producer.py` | producer Kafka dengan mTLS | Kode 13.1 |
| `envelope_encryption.py` | envelope encryption AES-GCM + rotasi KEK | Kode 13.2 |
| `abac.py` | mesin kebijakan ABAC sederhana | Kode 13.3 |
| `rls.sql` | row-level security dan column grant PostgreSQL | Kode 13.4 |
| `dp_laplace.py` | mekanisme Laplace (differential privacy) | Kode 13.5 |
| `presidio_tokenisasi.py` | tokenisasi HMAC + pembersihan teks bebas Presidio | Kode 13.6 |
| `crypto_shredding.py` | crypto-shredding dengan kunci per nasabah | Kode 13.7 |
| `spark_secure.py` | konfigurasi keamanan Spark + token Pandas UDF | Kode 13.8 |
| `rustfs_policy.sh` | kebijakan IAM per peran di RustFS (`rc`) dan uji penolakan | Kode 13.9 |
| `k_anonymity.py` | menghitung k dan l pada contoh tabel | Contoh di subbab 13.6 |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python envelope_encryption.py
python abac.py
python k_anonymity.py
python dp_laplace.py
python crypto_shredding.py
export TOKEN_KEY="$(openssl rand -hex 32)"   # key HMAC; di produksi dari Vault
python -m spacy download en_core_web_lg && python presidio_tokenisasi.py
psql -h localhost -U postgres -f rls.sql          # PostgreSQL 15+
```

`kafka_tls_producer.py` butuh broker Kafka dengan listener SSL dan sertifikat dari CA
internal; `spark_secure.py` butuh klaster Spark dan server S3 ber-TLS (RustFS di lab);
`rustfs_policy.sh` butuh RustFS dan klien `rc` (https://github.com/rustfs/cli). Nomor Kode mengikuti urutan di bab; periksa kembali bila bab disunting.
