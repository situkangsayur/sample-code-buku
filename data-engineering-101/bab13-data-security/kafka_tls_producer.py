"""Producer Kafka dengan mTLS. Butuh broker dengan listener SSL di port 9093
dan sertifikat yang ditandatangani CA internal (lihat README)."""
from confluent_kafka import Producer

p = Producer({
    "bootstrap.servers": "kafka:9093",
    "security.protocol": "SSL",
    "ssl.ca.location": "/certs/ca.crt",          # percayai CA internal
    # mTLS: identitas klien (dipasang dari Vault, bukan dari Git)
    "ssl.certificate.location": "/certs/corebanking.crt",
    "ssl.key.location": "/certs/corebanking.key",
    "enable.idempotence": True,
})


def laporan(err, msg):
    print("GAGAL:" if err else "terkirim:", err or msg.topic())


p.produce("transaksi", key=b"REK-001", value=b'{"nominal": 150000}',
          callback=laporan)
p.flush(10)
