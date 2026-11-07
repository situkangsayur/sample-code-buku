/* Kode 10.5-10.7: pertukaran dua arah.
 * mpirun -np 2 ./tukar <mode> <N>
 *   mode 0 = Send lalu Recv (bisa DEADLOCK untuk N besar)
 *   mode 1 = Ssend lalu Recv (selalu deadlock: alat uji)
 *   mode 2 = MPI_Sendrecv,  mode 3 = Isend/Irecv + Waitall                 */
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    int mode = argc > 1 ? atoi(argv[1]) : 2;
    int N = argc > 2 ? atoi(argv[2]) : 1000000;
    if (size != 2) { if (rank == 0) printf("jalankan dengan -np 2\n"); MPI_Finalize(); return 1; }
    double *kirim = malloc(N * sizeof(double)), *terima = malloc(N * sizeof(double));
    for (int i = 0; i < N; i++) kirim[i] = rank;
    int lawan = 1 - rank;
    if (mode == 0) {
        MPI_Send(kirim, N, MPI_DOUBLE, lawan, 0, MPI_COMM_WORLD);
        MPI_Recv(terima, N, MPI_DOUBLE, lawan, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    } else if (mode == 1) {
        MPI_Ssend(kirim, N, MPI_DOUBLE, lawan, 0, MPI_COMM_WORLD);
        MPI_Recv(terima, N, MPI_DOUBLE, lawan, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    } else if (mode == 2) {
        MPI_Sendrecv(kirim, N, MPI_DOUBLE, lawan, 0, terima, N, MPI_DOUBLE, lawan, 0,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    } else {
        MPI_Request req[2];
        MPI_Irecv(terima, N, MPI_DOUBLE, lawan, 0, MPI_COMM_WORLD, &req[0]);
        MPI_Isend(kirim, N, MPI_DOUBLE, lawan, 0, MPI_COMM_WORLD, &req[1]);
        /* di sini boleh menghitung hal lain, asal tidak menyentuh kirim/terima */
        MPI_Waitall(2, req, MPI_STATUSES_IGNORE);
    }
    printf("rank %d menerima nilai %.0f (mode %d, N=%d)\n", rank, terima[0], mode, N);
    free(kirim); free(terima);
    MPI_Finalize();
    return 0;
}
