"""Kode 5.6 dan Algoritma 5.1: consumer idempotent dengan tabel deduplication.

Contoh ini berdiri sendiri (SQLite, tanpa broker): kita menyimulasikan broker
at-least-once yang mengirim sebagian pesan dua kali, lalu menunjukkan bahwa
poin pelanggan tetap dihitung tepat sekali. Di produksi, tabelnya ada di
PostgreSQL dan pesan datang dari RabbitMQ/Kafka (lihat consumer_rabbit.py).

Pemakaian: python consumer_idempoten.py
"""
import random, sqlite3, uuid

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
CREATE TABLE pesan_diproses (id_pesan TEXT PRIMARY KEY);
CREATE TABLE poin (id_pelanggan INTEGER, id_pesanan INTEGER, jumlah INTEGER);
""")


def tangani(id_pesan: str, ev: dict) -> bool:
    """Kembalikan True bila efek diterapkan, False bila duplikat."""
    db.execute("BEGIN")
    cur = db.execute(
        "INSERT INTO pesan_diproses (id_pesan) VALUES (?) ON CONFLICT DO NOTHING",
        (id_pesan,))
    if cur.rowcount == 0:                # duplikat: batalkan, lalu tetap ack
        db.execute("ROLLBACK")
        return False
    db.execute("INSERT INTO poin VALUES (?, ?, ?)",
               (ev["pelanggan"], ev["pesanan"], ev["poin"]))
    db.execute("COMMIT")                 # efek dan catatan tersimpan bersama
    return True                          # setelah ini: ack / commit offset


def main():
    random.seed(7)
    pesan = [(str(uuid.uuid4()), {"pelanggan": 77, "pesanan": 1000 + i, "poin": 10})
             for i in range(100)]
    # broker at-least-once: sekitar 30% pesan terkirim dua kali, urutan diacak
    kiriman = pesan + random.sample(pesan, 30)
    random.shuffle(kiriman)
    diterapkan = sum(tangani(mid, ev) for mid, ev in kiriman)
    total = db.execute("SELECT SUM(jumlah) FROM poin").fetchone()[0]
    print(f"pesan diterima : {len(kiriman)}")
    print(f"efek diterapkan: {diterapkan} (duplikat diabaikan: {len(kiriman) - diterapkan})")
    print(f"total poin     : {total} (harus 1000)")
    assert total == 1000


if __name__ == "__main__":
    main()
