"""Kode 10.10: estimasi pi dengan mpi4py.  mpirun -np 4 python3 pi_mpi.py 100000000"""
import sys

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
h = 1.0 / n
lokal = 0.0
POTONG = 10_000_000                       # hitung per potongan agar memori hemat
for awal in range(rank, n, POTONG * size):
    i = np.arange(awal, min(awal + POTONG * size, n), size, dtype=np.float64)
    x = h * (i + 0.5)
    lokal += h * np.sum(4.0 / (1.0 + x * x))

pi = np.zeros(1)
comm.Allreduce(np.array([lokal]), pi, op=MPI.SUM)   # huruf besar: buffer NumPy
if rank == 0:
    print(f"pi ~ {pi[0]:.12f} dari {size} proses")
