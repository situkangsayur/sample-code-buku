"""Bab 40: satu entitas Mahasiswa sebagai object, baris tabel (SQLite), dokumen, dan JSON.

Hanya memakai library standar Python (dataclasses, json, sqlite3, base64).
Jalankan: python3 mahasiswa.py
"""
import base64
import json
import sqlite3
from dataclasses import asdict, dataclass, field


@dataclass
class Mahasiswa:
    nim: str
    nama: str
    prodi: str
    angkatan: int
    ipk: float
    email: str
    hobi: list = field(default_factory=list)

    def lulus_syarat_beasiswa(self) -> bool:
        return self.ipk >= 3.5


# ---------- JSON di API ----------
SCHEMA = {  # bentuk ringkas JSON Schema: nama field -> tipe Python yang diterima
    "nim": str, "nama": str, "prodi": str, "angkatan": int, "ipk": (int, float),
    "email": str, "hobi": list,
}


def to_json(m: Mahasiswa) -> str:
    return json.dumps(asdict(m), ensure_ascii=True, sort_keys=True)


def from_json(text: str) -> Mahasiswa:
    data = json.loads(text)
    for name, typ in SCHEMA.items():
        if name not in data:
            raise ValueError(f"field wajib hilang: {name}")
        if isinstance(data[name], bool) or not isinstance(data[name], typ):
            raise ValueError(f"tipe salah untuk {name}")
    if not (0.0 <= data["ipk"] <= 4.0):
        raise ValueError("ipk di luar 0..4")
    return Mahasiswa(**{k: data[k] for k in SCHEMA})


# ---------- Baris tabel dan index ----------
DDL = """
CREATE TABLE mahasiswa (
    nim      TEXT PRIMARY KEY,
    nama     TEXT NOT NULL,
    prodi    TEXT NOT NULL,
    angkatan INTEGER NOT NULL,
    ipk      REAL CHECK (ipk BETWEEN 0 AND 4),
    email    TEXT UNIQUE
);
CREATE TABLE hobi (nim TEXT REFERENCES mahasiswa(nim), hobi TEXT);
CREATE INDEX idx_mhs_prodi_angkatan ON mahasiswa(prodi, angkatan);
"""


def simpan(conn, m: Mahasiswa):
    conn.execute("INSERT INTO mahasiswa VALUES (?, ?, ?, ?, ?, ?)",
                 (m.nim, m.nama, m.prodi, m.angkatan, m.ipk, m.email))
    conn.executemany("INSERT INTO hobi VALUES (?, ?)", [(m.nim, h) for h in m.hobi])


def rencana(conn, sql, params=()):
    return [row[-1] for row in conn.execute("EXPLAIN QUERY PLAN " + sql, params)]


# ---------- Pagination ----------
def page_offset(conn, page, size):
    return conn.execute("SELECT nim FROM mahasiswa ORDER BY nim LIMIT ? OFFSET ?",
                        (size, page * size)).fetchall()


def encode_cursor(last_nim):
    return base64.urlsafe_b64encode(json.dumps({"after": last_nim}).encode()).decode()


def decode_cursor(cursor):
    return json.loads(base64.urlsafe_b64decode(cursor.encode()))["after"]


def page_cursor(conn, cursor, size):
    after = decode_cursor(cursor) if cursor else ""
    rows = conn.execute("SELECT nim FROM mahasiswa WHERE nim > ? ORDER BY nim LIMIT ?",
                        (after, size)).fetchall()
    nxt = encode_cursor(rows[-1][0]) if len(rows) == size else None
    return rows, nxt


def contoh_data(n):
    prodi = ["TI", "SI", "BD"]
    return [Mahasiswa(f"2027{i:04d}", f"Mhs {i}", prodi[i % 3], 2024 + i % 4,
                      round(2.5 + (i * 37 % 150) / 100, 2), f"m{i}@contoh.ac.id")
            for i in range(1, n + 1)]


if __name__ == "__main__":
    ani = Mahasiswa("20271001", "Ani Rahma", "TI", 2027, 3.75, "ani@contoh.ac.id",
                    ["catur", "panahan"])
    teks = to_json(ani)
    print(teks)
    assert from_json(teks) == ani                      # round trip
    for rusak in ['{"nim": 1}', teks.replace('"ipk": 3.75', '"ipk": 4.5'),
                  teks.replace('"angkatan": 2027', '"angkatan": "2027"')]:
        try:
            from_json(rusak)
            raise AssertionError("seharusnya ditolak")
        except ValueError as e:
            print("ditolak:", e)

    conn = sqlite3.connect(":memory:")
    conn.executescript(DDL)
    simpan(conn, ani)
    for m in contoh_data(1000):
        simpan(conn, m)

    q1 = "SELECT nama FROM mahasiswa WHERE prodi = ? AND angkatan = ?"
    q2 = "SELECT nama FROM mahasiswa WHERE ipk > ?"
    p1, p2 = rencana(conn, q1, ("TI", 2027)), rencana(conn, q2, (3.5,))
    print("rencana q1:", p1)
    print("rencana q2:", p2)
    assert "USING INDEX idx_mhs_prodi_angkatan" in p1[0] and p2[0].startswith("SCAN")

    # offset: baris baru di depan halaman menggeser isi halaman berikutnya
    hal0 = page_offset(conn, 0, 5)
    simpan(conn, Mahasiswa("20270000", "Baru", "TI", 2027, 3.0, "baru@contoh.ac.id"))
    hal1 = page_offset(conn, 1, 5)
    dobel = set(hal0) & set(hal1)
    print("offset: baris muncul dua kali =", dobel)
    assert dobel == {("20270005",)}

    conn.execute("DELETE FROM mahasiswa WHERE nim = '20270000'")
    rows, cur = page_cursor(conn, None, 5)
    simpan(conn, Mahasiswa("20270000", "Baru", "TI", 2027, 3.0, "baru@contoh.ac.id"))
    rows2, _ = page_cursor(conn, cur, 5)
    print("cursor:", cur, "->", rows2[0])
    assert not set(rows) & set(rows2) and rows2[0] == ("20270006",)

    # dokumen: hobi disimpan menempel, tanpa tabel kedua
    dokumen = asdict(ani) | {"_id": ani.nim}
    print("dokumen:", json.dumps(dokumen, sort_keys=True))
    hobi_tabel = [h for (h,) in conn.execute("SELECT hobi FROM hobi WHERE nim = ?", (ani.nim,))]
    assert hobi_tabel == dokumen["hobi"]
    print("semua uji mahasiswa lolos")
