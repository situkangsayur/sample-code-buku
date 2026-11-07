"""Idempotency key dengan transaksi SQLite.

Memanggil bayar("7f3a", "budi", 25000) berkali-kali hanya memotong saldo
sekali; panggilan berikutnya mengembalikan hasil yang tersimpan.

Jalankan:
    python bayar.py           # demo berurutan + uji tiga thread bersamaan
    python bayar.py --ulang   # hapus bayar.db lalu mulai dari saldo awal
"""
import hashlib
import json
import os
import sqlite3
import sys
import threading

BERKAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bayar.db")
if "--ulang" in sys.argv and os.path.exists(BERKAS):
    os.remove(BERKAS)


class _KoneksiPerThread:
    """Satu koneksi SQLite per thread.

    Koneksi SQLite tidak boleh dipakai bersama oleh banyak thread, dan transaksi
    milik satu koneksi tidak dapat berjalan paralel. Objek ini meneruskan
    execute/executescript ke koneksi milik thread pemanggil, sehingga fungsi
    bayar() di bawah tetap sama dengan versi di buku. Di buku, db cukup
    sqlite3.connect("bayar.db", isolation_level=None).
    """

    def __init__(self):
        self._lokal = threading.local()

    def _koneksi(self):
        if not hasattr(self._lokal, "c"):
            # isolation_level=None: kita mengatur BEGIN/COMMIT sendiri
            # timeout: tunggu kunci tulis milik thread lain, jangan langsung gagal
            self._lokal.c = sqlite3.connect(BERKAS, isolation_level=None, timeout=10)
        return self._lokal.c

    def execute(self, *args):
        return self._koneksi().execute(*args)

    def executescript(self, skrip):
        return self._koneksi().executescript(skrip)


db = _KoneksiPerThread()
db.executescript("""
CREATE TABLE IF NOT EXISTS idem (kunci TEXT PRIMARY KEY, sidik TEXT, hasil TEXT);
CREATE TABLE IF NOT EXISTS saldo (akun TEXT PRIMARY KEY, nilai INTEGER);
INSERT OR IGNORE INTO saldo VALUES ('budi', 100000);""")


def bayar(kunci: str, akun: str, jumlah: int) -> dict:
    sidik = hashlib.sha256(json.dumps([akun, jumlah]).encode()).hexdigest()
    db.execute("BEGIN IMMEDIATE")                        # kunci tulis: atomik
    try:
        baris = db.execute("SELECT sidik, hasil FROM idem WHERE kunci=?", (kunci,)).fetchone()
        if baris:                                        # kunci sudah pernah dipakai
            db.execute("ROLLBACK")
            if baris[0] != sidik:
                return {"status": 422, "pesan": "kunci dipakai untuk isi berbeda"}
            return json.loads(baris[1])                  # kembalikan hasil lama
        db.execute("UPDATE saldo SET nilai = nilai - ? WHERE akun = ?", (jumlah, akun))
        sisa = db.execute("SELECT nilai FROM saldo WHERE akun=?", (akun,)).fetchone()[0]
        hasil = {"status": 201, "sisa": sisa}
        db.execute("INSERT INTO idem VALUES (?,?,?)", (kunci, sidik, json.dumps(hasil)))
        db.execute("COMMIT")                             # efek + kunci bersama
        return hasil
    except Exception:
        db.execute("ROLLBACK")
        raise


def saldo(akun: str) -> int:
    return db.execute("SELECT nilai FROM saldo WHERE akun=?", (akun,)).fetchone()[0]


if __name__ == "__main__":
    print("saldo awal    :", saldo("budi"))
    print("bayar ke-1    :", bayar("7f3a", "budi", 25000))
    print("bayar ke-2    :", bayar("7f3a", "budi", 25000), "(retry: hasil lama)")
    print("isi berbeda   :", bayar("7f3a", "budi", 99000))
    print("saldo kini    :", saldo("budi"))

    # Uji bersamaan: tiga thread memakai kunci baru yang SAMA pada saat hampir
    # bersamaan. BEGIN IMMEDIATE membuat hanya satu yang memegang kunci tulis;
    # dua lainnya menunggu, lalu melihat kunci sudah ada.
    kunci_baru = os.urandom(4).hex()
    sebelum = saldo("budi")
    hasil, mulai = [], threading.Barrier(3)

    def kerja():
        mulai.wait()                                     # lepas tiga thread serentak
        hasil.append(bayar(kunci_baru, "budi", 10000))

    th = [threading.Thread(target=kerja) for _ in range(3)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    print(f"tiga thread   : {hasil}")
    print(f"saldo terpotong {sebelum - saldo('budi')} (harus 10000, bukan 30000)")
