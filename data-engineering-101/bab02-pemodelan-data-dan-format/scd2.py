"""SCD tipe 1 dan tipe 2 pada dim_nasabah dengan DuckDB (Kode 2.x)."""
import duckdb

con = duckdb.connect()
con.sql("""CREATE TABLE dim_nasabah (
  sk_nasabah INTEGER, id_nasabah VARCHAR, segmen VARCHAR, kota VARCHAR,
  berlaku_dari DATE, berlaku_sampai DATE, aktif BOOLEAN)""")
con.sql("CREATE SEQUENCE seq_sk START 101")
con.sql("""INSERT INTO dim_nasabah VALUES
  (nextval('seq_sk'), '7712', 'ritel', 'Bogor', DATE '2024-01-15', DATE '9999-12-31', true),
  (nextval('seq_sk'), '8820', 'UMKM',  'Bogor', DATE '2023-05-02', DATE '9999-12-31', true)""")

# Data hari ini dari sistem sumber (staging): 7712 pindah ke Bandung,
# 8820 hanya membetulkan ejaan segmen, 9001 nasabah baru.
con.sql("""CREATE TABLE stg_nasabah AS SELECT * FROM (VALUES
  ('7712', 'ritel', 'Bandung'), ('8820', 'umkm', 'Bogor'), ('9001', 'ritel', 'Depok'))
  t(id_nasabah, segmen, kota)""")
TGL = "DATE '2026-07-01'"

con.sql("BEGIN TRANSACTION")
# Tipe 1 untuk segmen: timpa nilai lama pada SEMUA versi baris.
con.sql("""UPDATE dim_nasabah d SET segmen = s.segmen
  FROM stg_nasabah s WHERE d.id_nasabah = s.id_nasabah AND d.segmen <> s.segmen""")
# Tipe 2 untuk kota langkah 1: tutup baris aktif yang kotanya berubah.
con.sql(f"""UPDATE dim_nasabah d
  SET berlaku_sampai = {TGL} - INTERVAL 1 DAY, aktif = false
  FROM stg_nasabah s
  WHERE d.id_nasabah = s.id_nasabah AND d.aktif AND d.kota <> s.kota""")
# Langkah 2: sisipkan versi baru untuk yang berubah dan nasabah yang belum ada.
con.sql(f"""INSERT INTO dim_nasabah
  SELECT nextval('seq_sk'), s.id_nasabah, s.segmen, s.kota, {TGL}, DATE '9999-12-31', true
  FROM stg_nasabah s
  LEFT JOIN dim_nasabah d ON d.id_nasabah = s.id_nasabah AND d.aktif
  WHERE d.id_nasabah IS NULL""")
con.sql("COMMIT")

print(con.sql("SELECT * FROM dim_nasabah ORDER BY id_nasabah, berlaku_dari"))
