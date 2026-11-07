-- Skema basis data inti bank untuk latihan CDC (Bab 10).
-- Dijalankan otomatis oleh container postgres saat pertama kali dibuat.

CREATE TABLE IF NOT EXISTS transaksi (
    id_trx       TEXT PRIMARY KEY,
    id_rekening  TEXT        NOT NULL,
    id_perangkat TEXT        NOT NULL,
    nominal      BIGINT      NOT NULL,
    waktu        TIMESTAMP   NOT NULL,       -- waktu kejadian (UTC), event time
    status       TEXT        NOT NULL DEFAULT 'SUKSES'
);

-- agar event UPDATE dan DELETE membawa isi "before" yang lengkap
ALTER TABLE transaksi REPLICA IDENTITY FULL;

-- Outbox pattern: data bisnis dan event ditulis dalam satu transaksi
CREATE TABLE IF NOT EXISTS akad (
    id_akad      TEXT PRIMARY KEY,
    id_nasabah   TEXT        NOT NULL,
    jenis        TEXT        NOT NULL,       -- mis. murabahah
    pokok        BIGINT      NOT NULL,
    margin       BIGINT      NOT NULL,
    dibuat       TIMESTAMP   NOT NULL DEFAULT now()
);

-- kolom mengikuti nama bawaan Debezium outbox event router
CREATE TABLE IF NOT EXISTS outbox (
    id            UUID PRIMARY KEY,
    aggregatetype TEXT  NOT NULL,            -- menentukan topik tujuan
    aggregateid   TEXT  NOT NULL,            -- menjadi key pesan Kafka
    type          TEXT  NOT NULL,            -- jenis event, mis. AkadDibuat
    payload       JSONB NOT NULL
);
