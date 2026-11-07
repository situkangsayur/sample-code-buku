# Bab 10 - Klaster HPC dan MPI

Contoh kode untuk Bab 10 buku *Sistem Terdistribusi dan Komputasi Berkinerja Tinggi*.
Butuh Open MPI atau MPICH (`mpicc`, `mpirun`) dan, untuk versi Python, `mpi4py` + NumPy.
Di PC lab Debian semuanya sudah terpasang; di laptop pakai `Dockerfile`.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `halo.c` | Kode 10.1-10.2 | Program MPI pertama (rank, size, nama mesin) |
| `hosts.txt` | Kode 10.3 | Hostfile untuk menjalankan di beberapa PC lab |
| `p2p.c` | Kode 10.5 | `MPI_Send`/`MPI_Recv`, `MPI_Status`, `MPI_Get_count` |
| `tukar.c` | Kode 10.6-10.8 | Deadlock (mode 0/1), `MPI_Sendrecv` (2), non-blocking (3) |
| `pi.c` | Kode 10.9-10.10 | Estimasi pi dengan `MPI_Reduce` |
| `pi_mpi.py` | Kode 10.11 | Estimasi pi dengan mpi4py `Allreduce` |
| `jacobi1d.c` | Kode 10.12 | Persamaan panas 1D dengan halo exchange (`MPI_PROC_NULL`) |
| `slurm/pi.sbatch` | Kode 10.13 | Job Slurm MPI |
| `slurm/hybrid.sbatch`, `hybrid.c` | Kode 10.15-10.16 | Job hybrid MPI + OpenMP |
| `Dockerfile` | Kode 10.17 | Lingkungan Open MPI di container |
| `pingpong.c` | Kode 10.18-10.19 | Ping-pong untuk mengukur alfa dan beta |

Nomor Kode mengikuti urutan di buku dan dapat bergeser sedikit bila buku direvisi.

## Menjalankan

```bash
# di laptop: container
docker build -t mpi-lab . && docker run --rm -it -v "$PWD":/kerja -w /kerja mpi-lab bash

make
mpirun -np 4 ./halo
mpirun -np 2 ./p2p
mpirun -np 2 ./tukar 2 1000000        # aman; mode 1 akan macet (tekan Ctrl-C)
make scaling                          # pi dengan 1, 2, 4, 8 proses
mpirun -np 4 python3 pi_mpi.py 100000000
for np in 1 2 4; do mpirun -np $np ./jacobi1d 1000000 2000; done
make pingpong-tcp                     # memori bersama vs TCP
OMP_NUM_THREADS=2 mpirun -np 2 ./hybrid

# di PC lab (SSH tanpa kata sandi, program ada di path yang sama di setiap PC)
mpirun --hostfile hosts.txt -np 16 ./halo
mpirun --hostfile hosts.txt --map-by node -np 2 ./pingpong
```

Kolom "jumlah suhu" pada `jacobi1d` harus sama untuk berapa pun jumlah proses.
