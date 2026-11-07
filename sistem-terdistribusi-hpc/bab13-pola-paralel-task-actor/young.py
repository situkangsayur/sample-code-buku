"""Selang checkpoint optimal menurut hampiran Young (1974): tau = sqrt(2 * C * M).

    python young.py --tulis-menit 5 --mtbf-jam 24
"""
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("--tulis-menit", type=float, required=True, help="C: lama menulis satu checkpoint")
ap.add_argument("--mtbf-jam", type=float, required=True, help="M: MTBF klaster")
a = ap.parse_args()
C, M = a.tulis_menit, a.mtbf_jam * 60
tau = math.sqrt(2 * C * M)
boros = C / tau + tau / (2 * M)       # porsi waktu: menulis + kerja yang hilang (perkiraan)
print(f"tau_opt ~ {tau:.1f} menit; porsi waktu terbuang ~ {100 * boros:.1f}%")
