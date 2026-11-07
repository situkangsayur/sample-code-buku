"""Hash chain: setiap catatan menyimpan hash catatan sebelumnya.
Mengubah satu catatan lama membuat verifikasi gagal mulai dari catatan itu.
"""
import hashlib
import json

GENESIS = "0" * 64


def h(prev: str, rec: dict) -> str:
    s = prev + json.dumps(rec, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest()


def bangun(records: list[dict]) -> list[tuple[dict, str]]:
    log, prev = [], GENESIS
    for r in records:
        prev = h(prev, r)
        log.append((dict(r), prev))
    return log


def verifikasi(log: list[tuple[dict, str]]) -> int | None:
    """Kembalikan indeks catatan pertama yang tidak cocok, atau None bila utuh."""
    prev = GENESIS
    for i, (r, hh) in enumerate(log):
        prev = h(prev, r)
        if prev != hh:
            return i
    return None


if __name__ == "__main__":
    akad = [{"akad": 1, "jenis": "murabahah", "nilai": 120_000_000},
            {"akad": 2, "jenis": "ijarah", "nilai": 75_000_000},
            {"akad": 3, "jenis": "musyarakah", "nilai": 300_000_000}]
    log = bangun(akad)
    print("root (hash terakhir):", log[-1][1][:16], "...")
    print("utuh? rusak di:", verifikasi(log))
    log[0][0]["nilai"] = 1_000            # admin menyunting diam-diam
    print("setelah disunting, rusak di indeks:", verifikasi(log))
