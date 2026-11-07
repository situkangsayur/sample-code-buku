"""Menguji logika Kode 11.5 tanpa server memakai chDB (ClickHouse tertanam).
Tabel Kafka diganti tabel Null dan klausa TTL TO VOLUME dihilangkan, karena keduanya
butuh broker dan storage policy server. Jalankan: python uji_clickhouse_chdb.py"""
from chdb import session

s = session.Session()
s.query("CREATE DATABASE IF NOT EXISTS uji ENGINE = Atomic")
s.query("""CREATE TABLE uji.trx_kafka (id_trx String, rekening String,
  cabang LowCardinality(String), nominal Decimal(18,2), event_time DateTime64(3)) ENGINE = Null""")
s.query("""CREATE TABLE uji.trx_per_menit (cabang LowCardinality(String), menit DateTime,
  jumlah UInt64, total Decimal(38,2)) ENGINE = SummingMergeTree ORDER BY (cabang, menit)
  TTL menit + INTERVAL 90 DAY DELETE""")
s.query("""CREATE MATERIALIZED VIEW uji.mv_trx TO uji.trx_per_menit AS
  SELECT cabang, toStartOfMinute(event_time) AS menit, count() AS jumlah, sum(nominal) AS total
  FROM uji.trx_kafka GROUP BY cabang, menit""")
for blok in range(3):    # tiga blok insert -> tiga part untuk menit yang sama
    s.query(f"""INSERT INTO uji.trx_kafka SELECT toString(number), 'R-1',
      if(number % 2 = 0, 'BDG', 'JKT'), 150000, now64(3) FROM numbers({blok * 10}, 10)""")
print("baris mentah (sebelum merge):")
print(s.query("SELECT cabang, menit, jumlah FROM uji.trx_per_menit ORDER BY cabang", "PrettyCompact"))
print("kueri yang benar (agregasi ulang):")
print(s.query("""SELECT cabang, sum(jumlah) AS jumlah_trx, sum(total) AS total_nominal
  FROM uji.trx_per_menit GROUP BY cabang ORDER BY cabang""", "PrettyCompact"))
