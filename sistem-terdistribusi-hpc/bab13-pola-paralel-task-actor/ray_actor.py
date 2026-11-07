"""Ray actor berkeadaan: satu Penghitung vs beberapa Penghitung (sharding sederhana).

    python ray_actor.py --panggilan 10000 --actor 1
    python ray_actor.py --panggilan 10000 --actor 4
"""
import argparse
import time

import ray


@ray.remote(max_restarts=2, max_task_retries=1)
class Penghitung:
    def __init__(self) -> None:
        self.n = 0                      # keadaan di memori: HILANG bila proses mati

    def tambah(self, k: int = 1) -> int:
        self.n += k
        return self.n

    def nilai(self) -> int:
        return self.n


@ray.remote
def pengirim(actors, mulai: int, jumlah: int) -> None:
    refs = []
    for i in range(mulai, mulai + jumlah):
        a = actors[i % len(actors)]      # sebar panggilan ke actor berdasarkan kunci i
        refs.append(a.tambah.remote())
    ray.get(refs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alamat", default=None)
    ap.add_argument("--panggilan", type=int, default=10_000)
    ap.add_argument("--actor", type=int, default=1)
    ap.add_argument("--pengirim", type=int, default=8)
    a = ap.parse_args()
    ray.init(address=a.alamat)
    actors = [Penghitung.remote() for _ in range(a.actor)]
    per = a.panggilan // a.pengirim
    t0 = time.perf_counter()
    ray.get([pengirim.remote(actors, i * per, per) for i in range(a.pengirim)])
    dt = time.perf_counter() - t0
    total = sum(ray.get([x.nilai.remote() for x in actors]))
    print(f"actor={a.actor} total={total} waktu={dt:.2f}s throughput={total / dt:.0f} panggilan/s")


if __name__ == "__main__":
    main()
