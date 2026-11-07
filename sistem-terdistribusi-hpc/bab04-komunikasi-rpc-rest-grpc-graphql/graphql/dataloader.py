"""DataLoader mini dengan asyncio, dan perbandingan resolver naif vs DataLoader.

Masalah N+1: query daftar produk (1 query) lalu satu query penjual untuk tiap
produk (N query). DataLoader mengumpulkan semua permintaan penjual dalam satu
putaran event loop lalu mengambilnya sekaligus: total 2 query.

Jalankan: python dataloader.py      (tanpa pustaka tambahan, Python 3.10+)
"""
import asyncio


class DataLoader:
    def __init__(self, ambil_banyak):
        self.ambil_banyak, self.antre, self.cache = ambil_banyak, {}, {}

    def muat(self, kunci):
        if kunci in self.cache:
            return self.cache[kunci]
        if not self.antre:                       # jadwalkan kirim sekali per putaran
            asyncio.get_running_loop().call_soon(lambda: asyncio.ensure_future(self._kirim()))
        fut = asyncio.get_running_loop().create_future()
        self.antre[kunci] = fut
        self.cache[kunci] = fut
        return fut

    async def _kirim(self):
        antre, self.antre = self.antre, {}
        try:
            hasil = await self.ambil_banyak(list(antre))     # SATU query untuk semua kunci
        except Exception as e:                   # teruskan error ke semua penunggu
            for fut in antre.values():
                fut.set_exception(e)
            return
        for k, fut in antre.items():
            fut.set_result(hasil.get(k))


# ---------------------------------------------------------------------------
# Basis data palsu: setiap query memakan 10 ms dan dicatat jumlahnya.
PRODUK = [{"id": i, "nama": f"Kopi {i}", "harga": 20000 + 500 * i, "penjual_id": 7 + i % 5}
          for i in range(1, 101)]
PENJUAL = {7 + j: {"id": 7 + j, "nama": f"Toko {chr(65 + j)}"} for j in range(5)}
jumlah_query = 0


async def query_produk(kategori):
    global jumlah_query
    jumlah_query += 1
    await asyncio.sleep(0.01)
    return PRODUK                                  # SELECT * FROM produk WHERE kategori=?


async def query_penjual(id_):
    global jumlah_query
    jumlah_query += 1
    await asyncio.sleep(0.01)
    return PENJUAL.get(id_)                        # SELECT * FROM penjual WHERE id=?


async def query_penjual_banyak(ids):
    global jumlah_query
    jumlah_query += 1
    await asyncio.sleep(0.01)
    print(f"  SELECT * FROM penjual WHERE id IN ({', '.join(map(str, ids))})")
    return {i: PENJUAL.get(i) for i in ids}


# ---------------------------------------------------------------------------
# Resolver untuk query GraphQL:
#   query { produk(kategori: "kopi") { nama harga penjual { nama } } }
async def resolve_naif(kategori):
    daftar = await query_produk(kategori)

    async def satu(p):                             # resolver field penjual
        return {"nama": p["nama"], "harga": p["harga"],
                "penjual": {"nama": (await query_penjual(p["penjual_id"]))["nama"]}}
    return await asyncio.gather(*(satu(p) for p in daftar))


async def resolve_dataloader(kategori):
    loader = DataLoader(query_penjual_banyak)      # satu loader per request
    daftar = await query_produk(kategori)

    async def satu(p):
        penjual = await loader.muat(p["penjual_id"])
        return {"nama": p["nama"], "harga": p["harga"], "penjual": {"nama": penjual["nama"]}}
    return await asyncio.gather(*(satu(p) for p in daftar))


async def main():
    global jumlah_query
    for nama, resolver in [("naif", resolve_naif), ("DataLoader", resolve_dataloader)]:
        jumlah_query = 0
        t0 = asyncio.get_running_loop().time()
        hasil = await resolver("kopi")
        dt = (asyncio.get_running_loop().time() - t0) * 1000
        print(f"{nama:10s}: {len(hasil)} produk, {jumlah_query} query basis data, {dt:.0f} ms")
        print(f"  contoh: {hasil[0]}")


if __name__ == "__main__":
    asyncio.run(main())
