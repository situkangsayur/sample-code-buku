"""Kode 11.10: rekonsiliasi harian agregat hot dan gold. Jalankan: python rekonsiliasi.py"""
import duckdb

def rekonsiliasi(con, tanggal: str, ambang_rel=0.005, ambang_abs=5):
    """hot_cabang_harian: ekspor agregat ClickHouse; gold_cabang_harian: lapis gold."""
    return con.execute("""
        WITH h AS (SELECT cabang, jumlah FROM hot_cabang_harian  WHERE tanggal = ?),
             g AS (SELECT cabang, jumlah FROM gold_cabang_harian WHERE tanggal = ?),
             b AS (SELECT coalesce(h.cabang, g.cabang) AS cabang,
                          coalesce(h.jumlah, 0) AS hot, coalesce(g.jumlah, 0) AS gold
                   FROM h FULL OUTER JOIN g ON h.cabang = g.cabang)
        SELECT cabang, hot, gold, abs(hot - gold) AS selisih,
               round(abs(hot - gold) / greatest(gold, 1), 4) AS rel
        FROM b
        WHERE abs(hot - gold) > ? AND abs(hot - gold) / greatest(gold, 1) > ?
        ORDER BY selisih DESC
    """, [tanggal, tanggal, ambang_abs, ambang_rel]).df()

if __name__ == "__main__":
    con = duckdb.connect()
    con.execute("""CREATE TABLE hot_cabang_harian AS SELECT * FROM (VALUES
        (DATE '2026-10-20','BDG',1492),(DATE '2026-10-20','JKT',20410),
        (DATE '2026-10-20','SBY',8820),(DATE '2026-10-20','MKS',12)) t(tanggal,cabang,jumlah)""")
    con.execute("""CREATE TABLE gold_cabang_harian AS SELECT * FROM (VALUES
        (DATE '2026-10-20','BDG',1476),(DATE '2026-10-20','JKT',20398),
        (DATE '2026-10-20','SBY',8821),(DATE '2026-10-20','MKS',10),
        (DATE '2026-10-20','PLG',940)) t(tanggal,cabang,jumlah)""")
    print(rekonsiliasi(con, "2026-10-20"))
