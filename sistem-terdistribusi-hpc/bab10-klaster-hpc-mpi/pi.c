/* Kode 10.8: estimasi pi dengan MPI.  mpirun -np 4 ./pi 1000000000 */
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    long n = (argc > 1) ? atol(argv[1]) : 100000000L;
    double h = 1.0 / n, lokal = 0.0, pi = 0.0;

    MPI_Barrier(MPI_COMM_WORLD);
    double t0 = MPI_Wtime();
    for (long i = rank; i < n; i += size) {
        double x = h * (i + 0.5);
        lokal += 4.0 / (1.0 + x * x);
    }
    lokal *= h;
    MPI_Reduce(&lokal, &pi, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    double t1 = MPI_Wtime();

    if (rank == 0)
        printf("pi ~ %.12f  waktu %.3f s  (%d proses)\n", pi, t1 - t0, size);
    MPI_Finalize();
    return 0;
}
