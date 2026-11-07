"""Kode 5.7 dan Algoritma 5.2: transactional outbox dan relay polling.

Basis data memakai SQLite agar mudah dijalankan; di produksi pakai PostgreSQL
(SELECT ... FOR UPDATE SKIP LOCKED). Relay menerbitkan ke RabbitMQ bila
AMQP_HOST tersedia, atau hanya mencetak bila dijalankan dengan --cetak.

Pemakaian:
  python outbox_relay.py --cetak        # tanpa broker
  python outbox_relay.py                # terbitkan ke RabbitMQ di localhost
"""
import json, os, sqlite3, sys, time, uuid

db = sqlite3.connect("pesanan.db", isolation_level=None)
db.executescript("""
CREATE TABLE IF NOT EXISTS pesanan (id INTEGER PRIMARY KEY, id_pelanggan INTEGER,
  total INTEGER, status TEXT);
CREATE TABLE IF NOT EXISTS outbox (id TEXT PRIMARY KEY, topik TEXT NOT NULL,
  kunci TEXT NOT NULL, isi TEXT NOT NULL,
  dibuat REAL NOT NULL, terkirim REAL);
""")


def buat_pesanan(id_pesanan: int, pelanggan: int, total: int) -> None:
    """Satu transaksi lokal: baris pesanan DAN event-nya, atau tidak keduanya."""
    ev = {"tipe": "PesananDibuat", "id_pesanan": id_pesanan, "total": total}
    db.execute("BEGIN")
    db.execute("INSERT OR IGNORE INTO pesanan VALUES (?, ?, ?, 'MENUNGGU')",
               (id_pesanan, pelanggan, total))
    db.execute("INSERT INTO outbox (id, topik, kunci, isi, dibuat) VALUES (?, ?, ?, ?, ?)",
               (str(uuid.uuid4()), "pesanan.dibuat", str(id_pesanan), json.dumps(ev), time.time()))
    db.execute("COMMIT")


def penerbit():
    if "--cetak" in sys.argv:
        return lambda e: print(f"[terbit] {e[1]} key={e[2]} id={e[0]} {e[3]}")
    import pika
    ch = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get("AMQP_HOST", "localhost"))).channel()
    ch.queue_declare(queue="pesanan.dibuat", durable=True)
    ch.confirm_delivery()                      # tunggu konfirmasi broker
    def terbit(e):
        ch.basic_publish("", e[1], e[3], pika.BasicProperties(
            delivery_mode=2, message_id=e[0]))
    return terbit


def relay(terbit, batch=50, jeda=0.5, putaran=3):
    for _ in range(putaran):                   # di produksi: loop tanpa akhir
        baris = db.execute("SELECT id, topik, kunci, isi FROM outbox WHERE terkirim IS NULL "
                           "ORDER BY dibuat LIMIT ?", (batch,)).fetchall()
        for e in baris:
            terbit(e)                          # at-least-once: bisa terbit ulang bila mati di sini
            db.execute("UPDATE outbox SET terkirim = ? WHERE id = ?", (time.time(), e[0]))
        if not baris:
            time.sleep(jeda)


if __name__ == "__main__":
    for i in range(5):
        buat_pesanan(1000 + i, 77, 25000 + i)
    relay(penerbit())
    sisa = db.execute("SELECT COUNT(*) FROM outbox WHERE terkirim IS NULL").fetchone()[0]
    print(f"outbox belum terkirim: {sisa}")
