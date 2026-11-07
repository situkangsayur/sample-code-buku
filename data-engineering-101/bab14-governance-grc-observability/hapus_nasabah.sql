-- Spark SQL dengan katalog Iceberg bernama 'lake'.
-- 1. Hapus baris di tabel aktif (silver dan gold yang memuat token nasabah)
DELETE FROM lake.silver.transaksi WHERE nasabah_token = 'tok_8f3a91c2';
DELETE FROM lake.gold.profil_nasabah WHERE nasabah_token = 'tok_8f3a91c2';

-- 2. Snapshot lama masih menyimpan baris itu: akhiri snapshot lama
CALL lake.system.expire_snapshots(
  table => 'silver.transaksi',
  older_than => TIMESTAMP '2026-12-28 00:00:00',
  retain_last => 1);

-- 3. Bersihkan berkas yang tidak lagi dirujuk metadata
CALL lake.system.remove_orphan_files(table => 'silver.transaksi');

-- 4. Jangan lupa: serving store, cache BI, dan backup (crypto-shredding, Bab 13).
