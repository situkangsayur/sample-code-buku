-- PostgreSQL: tabel jurnal append-only dengan hash chain (butuh ekstensi pgcrypto).
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE jurnal_akad (
  id         bigserial PRIMARY KEY,
  isi        jsonb       NOT NULL,
  dibuat     timestamptz NOT NULL DEFAULT now(),
  hash_prev  bytea       NOT NULL,
  hash       bytea       NOT NULL
);

-- hash = sha256(hash_prev || isi), dihitung otomatis saat INSERT
CREATE FUNCTION jurnal_isi_hash() RETURNS trigger AS $$
DECLARE prev bytea;
BEGIN
  LOCK TABLE jurnal_akad IN SHARE ROW EXCLUSIVE MODE;    -- urutan rantai tunggal
  SELECT hash INTO prev FROM jurnal_akad ORDER BY id DESC LIMIT 1;
  NEW.hash_prev := coalesce(prev, '\x00'::bytea);
  NEW.hash := digest(NEW.hash_prev || convert_to(NEW.isi::text, 'UTF8'), 'sha256');
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER t_jurnal BEFORE INSERT ON jurnal_akad
  FOR EACH ROW EXECUTE FUNCTION jurnal_isi_hash();

-- aplikasi hanya boleh menambah
REVOKE UPDATE, DELETE, TRUNCATE ON jurnal_akad FROM PUBLIC;

-- root harian untuk diterbitkan ke luar (surel auditor, bucket object lock)
SELECT encode(hash, 'hex') AS root_hari_ini FROM jurnal_akad ORDER BY id DESC LIMIT 1;
