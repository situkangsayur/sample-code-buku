/* Kode 10.16: kerangka hybrid MPI + OpenMP (estimasi pi).
 * mpicc -O2 -fopenmp hybrid.c -o hybrid
 * OMP_NUM_THREADS=2 mpirun -np 2 ./hybrid                                */
#include <mpi.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int tingkat, rank, size;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &tingkat);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    long n = argc > 1 ? atol(argv[1]) : 1000000000L;
    double h = 1.0 / n;
    long awal = rank * (n / size), akhir = (rank == size - 1) ? n : awal + n / size;

    double t0 = MPI_Wtime(), lokal = 0.0;
    #pragma omp parallel for reduction(+:lokal)
    for (long i = awal; i < akhir; i++) {
        double x = (i + 0.5) * h;
        lokal += 4.0 / (1.0 + x * x);
    }
    double total;
    MPI_Allreduce(&lokal, &total, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    if (rank == 0)
        printf("pi ~ %.12f, %d rank x %d thread, %.3f s (tingkat thread %d)\n",
               total * h, size, omp_get_max_threads(), MPI_Wtime() - t0, tingkat);
    MPI_Finalize();
    return 0;
}
