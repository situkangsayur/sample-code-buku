/* Kode 10.11: persamaan panas 1D (Jacobi) dengan halo exchange.
 * mpirun -np 4 ./jacobi1d <N_global> <langkah>
 * Batang panjang N: ujung kiri 100 derajat, ujung kanan 0 derajat.         */
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    long N = argc > 1 ? atol(argv[1]) : 1000000;
    int T = argc > 2 ? atoi(argv[2]) : 1000;
    const double rc = 0.25;                     /* stabil bila <= 0.5 */

    /* pembagian blok: m titik lokal, sisa dibagi ke rank awal */
    int m = N / size + (rank < N % size ? 1 : 0);
    double *u = calloc(m + 2, sizeof(double)), *un = calloc(m + 2, sizeof(double));
    int kiri  = (rank > 0)        ? rank - 1 : MPI_PROC_NULL;
    int kanan = (rank < size - 1) ? rank + 1 : MPI_PROC_NULL;
    if (rank == 0) u[0] = 100.0;                /* batas global kiri  */
    if (rank == size - 1) u[m + 1] = 0.0;       /* batas global kanan */

    MPI_Barrier(MPI_COMM_WORLD);
    double t0 = MPI_Wtime();
    for (int t = 0; t < T; t++) {
        MPI_Sendrecv(&u[1], 1, MPI_DOUBLE, kiri, 0, &u[m + 1], 1, MPI_DOUBLE, kanan, 0,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Sendrecv(&u[m], 1, MPI_DOUBLE, kanan, 1, &u[0], 1, MPI_DOUBLE, kiri, 1,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        for (int i = 1; i <= m; i++)
            un[i] = u[i] + rc * (u[i - 1] - 2.0 * u[i] + u[i + 1]);
        un[0] = u[0]; un[m + 1] = u[m + 1];
        double *tmp = u; u = un; un = tmp;
    }
    double t1 = MPI_Wtime();

    /* checksum: jumlah suhu seluruh batang (harus sama untuk berapa pun np) */
    double lokal = 0.0, total = 0.0;
    for (int i = 1; i <= m; i++) lokal += u[i];
    MPI_Reduce(&lokal, &total, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    if (rank == 0)
        printf("N=%ld T=%d np=%d waktu %.3f s, jumlah suhu %.6f\n", N, T, size, t1 - t0, total);
    free(u); free(un);
    MPI_Finalize();
    return 0;
}
