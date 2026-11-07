/* tulis_bersama.c - setiap rank menulis bagiannya ke SATU berkas bersama dengan
 * collective I/O (MPI_File_write_at_all).
 * Kompilasi: make ; Jalankan: mpirun -np 4 ./tulis_bersama 8388608
 */
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);
  int rank, p;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &p);
  long n = (argc > 1) ? atol(argv[1]) : 1L << 23;   /* double per rank */
  double *buf = malloc(n * sizeof(double));
  for (long i = 0; i < n; ++i) buf[i] = rank * 1.0e9 + i;  /* "hasil" komputasi */

  MPI_File fh;
  MPI_File_open(MPI_COMM_WORLD, "hasil.bin",
                MPI_MODE_CREATE | MPI_MODE_WRONLY, MPI_INFO_NULL, &fh);
  MPI_Offset off = (MPI_Offset)rank * n * sizeof(double); /* tiap rank punya wilayah */
  double t0 = MPI_Wtime();
  /* _all = collective: library boleh menggabungkan potongan kecil menjadi tulisan besar */
  MPI_File_write_at_all(fh, off, buf, (int)n, MPI_DOUBLE, MPI_STATUS_IGNORE);
  MPI_File_close(&fh);
  double t = MPI_Wtime() - t0, tmaks;
  MPI_Reduce(&t, &tmaks, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
  if (rank == 0) {
    double mb = (double)p * n * sizeof(double) / 1e6;
    printf("%d rank menulis %.0f MB dalam %.3f s (%.0f MB/s)\n", p, mb, tmaks, mb / tmaks);
  }
  free(buf);
  MPI_Finalize();
  return 0;
}
