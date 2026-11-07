-- Kode 10.11: aturan fraud dalam Flink SQL (pembanding).
-- Jalankan di Flink SQL Client dengan konektor Kafka di classpath.
-- Topik bank.transaksi diisi oleh producer_transaksi.py (Kode 10.1), yang mengirim
-- id_perangkat dan event_time berformat "yyyy-MM-dd HH:mm:ss.SSS" (bawaan format JSON Flink).
-- Contoh isi topik: python producer_transaksi.py --jumlah 5000
CREATE TABLE transaksi (
  id_rekening  STRING,
  id_perangkat STRING,
  nominal      BIGINT,
  event_time   TIMESTAMP(3),
  WATERMARK FOR event_time AS event_time - INTERVAL '2' MINUTE
) WITH ('connector' = 'kafka', 'topic' = 'bank.transaksi',
        'properties.bootstrap.servers' = 'redpanda:9092', 'format' = 'json',
        'scan.startup.mode' = 'earliest-offset');

SELECT window_start, id_rekening, COUNT(*) AS n_trx,
       COUNT(DISTINCT id_perangkat) AS n_perangkat
FROM TABLE(TUMBLE(TABLE transaksi, DESCRIPTOR(event_time), INTERVAL '1' MINUTE))
GROUP BY window_start, window_end, id_rekening
HAVING COUNT(*) > 5 AND COUNT(DISTINCT id_perangkat) > 1;
