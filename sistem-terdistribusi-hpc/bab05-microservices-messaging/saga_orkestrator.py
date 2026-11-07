"""Algoritma 5.3: orchestrator saga dengan kompensasi.

Simulasi dalam satu proses: tiga 'layanan' (pesanan, stok, pembayaran) dengan
state masing-masing. Status saga disimpan ke berkas JSON (penyimpanan tahan lama)
agar terlihat jejak langkahnya.

Pemakaian:
  python saga_orkestrator.py            # pembayaran berhasil
  python saga_orkestrator.py gagal      # pembayaran gagal -> kompensasi berjalan
"""
import json, sys

pesanan, stok, saldo = {}, {"buku": 3}, {"ani": 30000}
GAGAL_BAYAR = "gagal" in sys.argv


def buat_pesanan(s):   pesanan[s["id"]] = "MENUNGGU"
def batalkan_pesanan(s): pesanan[s["id"]] = "DIBATALKAN"
def pesan_stok(s):
    if stok[s["barang"]] < 1: raise RuntimeError("stok habis")
    stok[s["barang"]] -= 1
def lepas_stok(s):     stok[s["barang"]] += 1
def tagih(s):
    if GAGAL_BAYAR or saldo[s["pelanggan"]] < s["total"]:
        raise RuntimeError("pembayaran ditolak")
    saldo[s["pelanggan"]] -= s["total"]
def konfirmasi(s):     pesanan[s["id"]] = "DIKONFIRMASI"

LANGKAH = [(buat_pesanan, batalkan_pesanan), (pesan_stok, lepas_stok),
           (tagih, None),               # pivot: setelah ini tidak dikompensasi
           (konfirmasi, None)]


def simpan(status):
    with open("saga_status.json", "w") as f:
        json.dump(status, f)


def jalankan_saga(s):
    selesai = []
    for i, (t, c) in enumerate(LANGKAH):
        try:
            t(s)                         # di dunia nyata: command + retry, t idempotent
            selesai.append(i)
            simpan({"saga": s["id"], "selesai": selesai})
            print(f"  T{i+1} {t.__name__}: ok")
        except Exception as e:
            print(f"  T{i+1} {t.__name__}: GAGAL ({e})")
            for j in reversed(selesai):
                komp = LANGKAH[j][1]
                if komp:
                    komp(s)              # kompensasi harus diulang sampai berhasil
                    print(f"  C{j+1} {komp.__name__}: ok")
            simpan({"saga": s["id"], "status": "dibatalkan"})
            return False
    simpan({"saga": s["id"], "status": "selesai"})
    return True


if __name__ == "__main__":
    saga = {"id": 1001, "barang": "buku", "pelanggan": "ani", "total": 25000}
    print("saga berhasil" if jalankan_saga(saga) else "saga dibatalkan")
    print("pesanan:", pesanan, "stok:", stok, "saldo:", saldo)
