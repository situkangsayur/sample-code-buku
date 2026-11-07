-- Kode 11.4: perawatan tabel Iceberg (Spark SQL dengan katalog bernama lake).
-- spark-sql -f iceberg_maintenance.sql  (ganti tanggal sesuai partisi yang dirawat)
-- 1. gabungkan berkas kecil menjadi berkas sekitar 256 MB
CALL lake.system.rewrite_data_files(
  table   => 'bronze.transaksi',
  where   => 'tanggal = "2026-10-21"',
  options => map('target-file-size-bytes', '268435456',
                 'min-input-files', '5',
                 'partial-progress.enabled', 'true'));

-- 2. rapikan manifest agar perencanaan kueri cepat
CALL lake.system.rewrite_manifests('bronze.transaksi');

-- 3. buang snapshot lama, sisakan 7 hari untuk time travel
CALL lake.system.expire_snapshots(
  table       => 'bronze.transaksi',
  older_than  => TIMESTAMP '2026-10-15 00:00:00',
  retain_last => 50);

-- 4. hapus berkas yatim dari job yang gagal di tengah jalan
CALL lake.system.remove_orphan_files(
  table      => 'bronze.transaksi',
  older_than => TIMESTAMP '2026-10-19 00:00:00');
