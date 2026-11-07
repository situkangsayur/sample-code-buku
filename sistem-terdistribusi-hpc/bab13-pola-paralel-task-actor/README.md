# Bab 13 - Pola Paralel, Task, dan Actor Terdistribusi

Contoh kode untuk Bab 13 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.

| Berkas / folder | Isi | Kaitan di buku |
|---|---|---|
| `rust-forkjoin/` | Fork-join (merge sort) dan map-reduce dengan Rayon (work stealing) | Kode 13.1 |
| `dask_berkas.py`, `buat_data.py` | Map-reduce atas ratusan berkas CSV dengan `dask.delayed` | Kode 13.2 |
| `ray_pi.py` | Monte Carlo pi dengan Ray task; strong/weak scaling, pengaruh jumlah task | Kode 13.3 |
| `ray_actor.py` | Ray actor berkeadaan; 1 vs banyak actor; `max_restarts` | Kode 13.4 |
| `ray_placement.py` | Placement group PACK/SPREAD | Kode 13.5 |
| `pekko-sharding/` | Apache Pekko Cluster Sharding (Scala): satu entity actor per rekening | Kode 13.6 |
| `mpiio/` | Collective I/O dengan MPI-IO ke satu berkas bersama | Kode 13.7 |
| `young.py` | Selang checkpoint optimal (Young) | Subbab checkpoint |
| `docker-compose.yml` | Klaster Ray dan Dask kecil di satu mesin | Kode 13.8 |

## Python (Ray, Dask)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python ray_pi.py --mode strong --sampel 100000000 --task 64     # Ray lokal
python buat_data.py --berkas 500
python dask_berkas.py --serial                                  # pembanding satu proses
python dask_berkas.py                                           # klaster Dask lokal
python ray_actor.py --actor 1 && python ray_actor.py --actor 4
```

Dengan klaster Docker (versi Python dan Ray/Dask klien harus sama dengan image):

```bash
docker compose up -d --scale ray-worker=2 --scale dask-worker=2
python ray_pi.py --alamat ray://localhost:10001 --task 64
python dask_berkas.py --alamat tcp://localhost:8786 --akar-worker /data
# dashboard: Ray http://localhost:8265, Dask http://localhost:8787
docker compose kill ray-worker      # uji kegagalan saat eksperimen berjalan
```

## Rust (Rayon)

```bash
cd rust-forkjoin && cargo run --release -- 20000000
```

Perhatikan: merge sort buatan sendiri hampir tidak lebih cepat daripada versi serial karena
langkah `gabung` di setiap tingkat masih serial (span-nya O(n)). `par_sort_unstable` dari Rayon
memparalelkan juga penggabungannya. Ini contoh nyata model work-span di Bab 13.

## Scala (Apache Pekko Cluster Sharding)

Butuh JDK 17+ dan sbt.

```bash
cd pekko-sharding
sbt "run 25520"            # terminal 1: node seed
sbt "run 25521 kirim"      # terminal 2: node kedua, mengirim setoran tiap 3 detik
sbt "run 25522"            # terminal 3: node ketiga; lalu matikan salah satu node
```

Log `entity 123 hidup di ...` menunjukkan node tempat entity berada. Saat node itu dimatikan,
entity dibuat ulang di node lain dan saldonya kembali 0, karena contoh ini tidak memakai
persistence (event sourcing). Itulah yang dibahas di buku.

## C (MPI-IO)

```bash
cd mpiio && make && mpirun -np 4 ./tulis_bersama 8388608
```
