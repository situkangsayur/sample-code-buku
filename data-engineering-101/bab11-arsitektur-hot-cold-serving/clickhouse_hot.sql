-- Kode 11.5: jalur Kafka -> materialized view -> SummingMergeTree di ClickHouse.
-- Volume 'dingin' didefinisikan di clickhouse/storage.xml (dipasang oleh docker-compose).
-- 1. penampung yang membaca topik (tidak menyimpan data)
CREATE TABLE trx_kafka (
  id_trx String, rekening String, cabang LowCardinality(String),
  nominal Decimal(18,2), event_time DateTime64(3)
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'redpanda:9092',
         kafka_topic_list  = 'bank.transaksi',
         kafka_group_name  = 'ch-hot',
         kafka_format      = 'JSONEachRow';

-- 2. tabel agregat; baris dengan kunci sama dijumlahkan saat merge
CREATE TABLE trx_per_menit (
  cabang LowCardinality(String), menit DateTime,
  jumlah UInt64, total Decimal(38,2)
) ENGINE = SummingMergeTree
ORDER BY (cabang, menit)
TTL menit + INTERVAL 7 DAY TO VOLUME 'dingin',
    menit + INTERVAL 90 DAY DELETE;

-- 3. materialized view: dipicu setiap blok yang dibaca dari Kafka
CREATE MATERIALIZED VIEW mv_trx TO trx_per_menit AS
SELECT cabang,
       toStartOfMinute(event_time) AS menit,
       count()                     AS jumlah,
       sum(nominal)                AS total
FROM trx_kafka
GROUP BY cabang, menit;

-- kueri dasbor: selalu agregasikan lagi karena merge bersifat malas
SELECT cabang, sum(jumlah) AS jumlah_trx, sum(total) AS total_nominal
FROM trx_per_menit
WHERE menit >= today()
GROUP BY cabang
ORDER BY jumlah_trx DESC;
