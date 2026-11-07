"""Kode 10.5: mendaftarkan connector Debezium PostgreSQL lewat REST API Kafka Connect.

Versi lengkap: menunggu Kafka Connect siap, mendaftarkan (atau memperbarui)
connector CDC tabel transaksi, opsional connector outbox, lalu menampilkan status.

Pemakaian:
    python daftar_connector.py            # connector bank-cdc
    python daftar_connector.py --outbox   # tambah connector outbox (pembiayaan.akad)
    python daftar_connector.py --hapus    # hapus semua connector latihan
"""
import argparse
import time

import requests

CONNECT = "http://localhost:8083"

cfg = {
  "name": "bank-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres", "database.port": "5432",
    "database.user": "postgres", "database.password": "rahasia_lab",
    "database.dbname": "bank",
    "topic.prefix": "bank",                 # topik: bank.public.transaksi
    "plugin.name": "pgoutput",
    "slot.name": "bank_cdc",                # replication slot di PostgreSQL
    "publication.autocreate.mode": "filtered",
    "table.include.list": "public.transaksi",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
  },
}

# Outbox pattern: baris tabel outbox diterbitkan ke topik pembiayaan.<aggregatetype>
cfg_outbox = {
  "name": "bank-outbox",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres", "database.port": "5432",
    "database.user": "postgres", "database.password": "rahasia_lab",
    "database.dbname": "bank",
    "topic.prefix": "bankoutbox",
    "plugin.name": "pgoutput",
    "slot.name": "bank_outbox",
    "publication.name": "bank_outbox_pub",
    "publication.autocreate.mode": "filtered",
    "table.include.list": "public.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.route.topic.replacement": "pembiayaan.${routedByValue}",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
  },
}


def tunggu_connect(batas=120):
    """Kafka Connect butuh beberapa detik sampai REST API siap."""
    akhir = time.time() + batas
    while time.time() < akhir:
        try:
            if requests.get(CONNECT, timeout=3).ok:
                return
        except requests.ConnectionError:
            pass
        print("menunggu Kafka Connect ...")
        time.sleep(3)
    raise SystemExit("Kafka Connect tidak menjawab; cek 'docker compose logs connect'")


def daftar(c):
    # PUT /connectors/<nama>/config bersifat idempotent: buat baru atau perbarui
    r = requests.put(f"{CONNECT}/connectors/{c['name']}/config",
                     json=c["config"], timeout=10)
    print(c["name"], r.status_code, r.json().get("name", r.text))


def status(nama):
    time.sleep(3)
    r = requests.get(f"{CONNECT}/connectors/{nama}/status", timeout=10)
    s = r.json()
    tugas = [t["state"] for t in s.get("tasks", [])]
    print(f"{nama}: connector={s.get('connector', {}).get('state')} task={tugas}")
    for t in s.get("tasks", []):
        if t["state"] == "FAILED":
            print(t.get("trace", "")[:800])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outbox", action="store_true")
    ap.add_argument("--hapus", action="store_true")
    a = ap.parse_args()

    tunggu_connect()
    if a.hapus:
        for nama in ("bank-cdc", "bank-outbox"):
            r = requests.delete(f"{CONNECT}/connectors/{nama}", timeout=10)
            print("hapus", nama, r.status_code)
        print("Catatan: replication slot tetap ada di PostgreSQL. Hapus dengan "
              "SELECT pg_drop_replication_slot('bank_cdc');")
        return

    daftar(cfg)
    status("bank-cdc")
    if a.outbox:
        daftar(cfg_outbox)
        status("bank-outbox")


if __name__ == "__main__":
    main()
