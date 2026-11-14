"""Bab 35: membaca EXPLAIN QUERY PLAN di SQLite (modul sqlite3 bawaan Python).

Diuji dengan SQLite 3.45.1 (Python 3.12.3). Teks rencana dapat sedikit
berbeda di versi SQLite lain; uji memeriksa kata kunci SCAN dan SEARCH.
"""
import sqlite3


def rencana(con, sql):
    return [baris[3] for baris in con.execute("EXPLAIN QUERY PLAN " + sql)]


def siapkan():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE mahasiswa (nim INTEGER PRIMARY KEY, nama TEXT,"
                " prodi TEXT, ipk REAL)")
    con.executemany("INSERT INTO mahasiswa VALUES (?, ?, ?, ?)",
                    [(i, "m%d" % i, ["TI", "SI", "MB"][i % 3], 2 + (i % 200) / 100)
                     for i in range(1, 10_001)])
    return con


if __name__ == "__main__":
    print("SQLite", sqlite3.sqlite_version)
    con = siapkan()
    q = "SELECT * FROM mahasiswa WHERE nama = 'm77'"

    sebelum = rencana(con, q)
    print("sebelum index :", sebelum)
    assert sebelum[0].startswith("SCAN mahasiswa")          # baca semua baris

    pk = rencana(con, "SELECT * FROM mahasiswa WHERE nim = 77")
    print("primary key   :", pk)
    assert pk[0].startswith("SEARCH mahasiswa USING INTEGER PRIMARY KEY")

    con.execute("CREATE INDEX idx_nama ON mahasiswa(nama)")  # B-tree baru
    sesudah = rencana(con, q)
    print("sesudah index :", sesudah)
    assert sesudah[0].startswith("SEARCH mahasiswa USING INDEX idx_nama")

    rentang = rencana(con, "SELECT nama FROM mahasiswa WHERE nama >= 'm7' AND nama < 'm8'")
    print("rentang       :", rentang)
    assert "COVERING INDEX idx_nama" in rentang[0]

    hasil = con.execute(q).fetchall()
    assert hasil == [(77, "m77", "MB", 2.77)]
    print("explain_sqlite: semua uji lolos")
