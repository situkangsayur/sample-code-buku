"""Placement group: PACK vs SPREAD. Jalankan di klaster beberapa node agar bedanya terlihat.

    python ray_placement.py --strategi SPREAD
"""
import argparse
import socket

import ray
from ray.util.placement_group import placement_group, remove_placement_group
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy


@ray.remote(num_cpus=1)
def di_mana(i: int) -> str:
    return f"bundle {i} di {socket.gethostname()}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alamat", default=None)
    ap.add_argument("--strategi", default="SPREAD",
                    choices=["PACK", "SPREAD", "STRICT_PACK", "STRICT_SPREAD"])
    ap.add_argument("--bundle", type=int, default=4)
    a = ap.parse_args()
    ray.init(address=a.alamat)
    pg = placement_group([{"CPU": 1}] * a.bundle, strategy=a.strategi)
    ray.get(pg.ready(), timeout=60)     # STRICT_* gagal di sini bila tidak terpenuhi
    refs = [di_mana.options(
                scheduling_strategy=PlacementGroupSchedulingStrategy(
                    placement_group=pg, placement_group_bundle_index=i)
            ).remote(i) for i in range(a.bundle)]
    for baris in ray.get(refs):
        print(baris)
    remove_placement_group(pg)


if __name__ == "__main__":
    main()
