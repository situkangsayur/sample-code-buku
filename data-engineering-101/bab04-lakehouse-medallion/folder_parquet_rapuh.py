"""Kode 4.1 dan 4.2: mengapa folder berisi Parquet belum menjadi tabel.

Penulis menimpa partisi berkas demi berkas. Pembaca yang datang di tengah
jalan melihat campuran versi lama dan baru; penulis yang gagal di tengah
meninggalkan partisi setengah jadi. Tidak ada yang mencatat berkas mana
yang sah.
"""
import pathlib
import shutil

import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

PART = pathlib.Path("folder_polos/trx/tanggal=2026-11-01")


def tulis_versi(versi: int, berkas: int, gagal_setelah: int | None = None):
    for i in range(berkas):
        if gagal_setelah is not None and i == gagal_setelah:
            raise RuntimeError(f"job versi {versi} mati setelah {i} berkas")
        t = pa.table({"id_trx": list(range(i * 1000, (i + 1) * 1000)),
                      "versi": [versi] * 1000})
        pq.write_table(t, PART / f"part-{i}.parquet")    # timpa satu berkas
        if versi == 2 and i == 1:
            baca("pembaca di tengah penulisan")            # dashboard membaca


def baca(siapa: str):
    t = ds.dataset(PART, format="parquet").to_table()
    hitung = t.group_by("versi").aggregate([("id_trx", "count")]).to_pylist()
    print(f"{siapa:32s} baris={t.num_rows:5d} per versi={hitung}")


if __name__ == "__main__":
    shutil.rmtree("folder_polos", ignore_errors=True)
    PART.mkdir(parents=True)
    tulis_versi(1, 4)
    baca("setelah versi 1")
    tulis_versi(2, 4)                       # di dalamnya ada pembaca
    baca("setelah versi 2")
    try:
        tulis_versi(3, 4, gagal_setelah=2)  # job koreksi gagal
    except RuntimeError as e:
        print("GAGAL:", e)
    baca("setelah versi 3 gagal")
