"""Kode 4.6, 4.7, dan Algoritma 4.1: optimistic concurrency control pada commit
tabel lakehouse, disimulasikan di memori.

Katalog hanya menyimpan satu pointer (versi metadata terbaru) dan menyediakan
compare-and-swap (CAS). Penulis menyiapkan metadata baru tanpa mengunci, lalu
CAS. Bila gagal, penulis membaca versi terbaru, memeriksa konflik, mencoba lagi.
"""
import random
import threading
import time


class Katalog:
    def __init__(self):
        self._kunci = threading.Lock()      # hanya melindungi satu pointer
        self.versi = 0
        self.riwayat = {0: frozenset()}     # versi -> partisi yang pernah diubah

    def baca(self):
        return self.versi

    def cas(self, harap: int, baru_partisi: set) -> bool:
        with self._kunci:                   # operasi atomik di katalog
            if self.versi != harap:
                return False
            self.versi += 1
            self.riwayat[self.versi] = frozenset(baru_partisi)
            return True


def commit(kat: Katalog, nama: str, partisi: set, maks_coba: int = 10):
    dasar = kat.baca()
    for coba in range(1, maks_coba + 1):
        time.sleep(random.uniform(0.001, 0.005))  # tulis Parquet + manifest
        if kat.cas(dasar, partisi):
            return f"{nama}: commit v{dasar + 1} pada percobaan {coba}"
        terbaru = kat.baca()
        for v in range(dasar + 1, terbaru + 1):   # validasi: konflik?
            if kat.riwayat[v] & partisi:
                return f"{nama}: BATAL, partisi {set(kat.riwayat[v] & partisi)} diubah v{v}"
        dasar = terbaru                           # tak konflik: rebase, ulangi
    return f"{nama}: menyerah setelah {maks_coba} percobaan"


if __name__ == "__main__":
    random.seed(4)
    kat = Katalog()
    tugas = {"ingest-01": {"2026-11-01"}, "ingest-02": {"2026-11-02"},
             "ingest-03": {"2026-11-03"}, "koreksi-01": {"2026-11-01"}}
    hasil = []
    th = [threading.Thread(target=lambda n=n, p=p: hasil.append(commit(kat, n, p)))
          for n, p in tugas.items()]
    for t in th: t.start()
    for t in th: t.join()
    print("\n".join(sorted(hasil)))
    print("versi akhir katalog:", kat.versi)
