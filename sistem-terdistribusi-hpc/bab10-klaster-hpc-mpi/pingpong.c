/* Kode 10.17: ping-pong untuk mengukur alfa dan beta.  mpirun -np 2 ./pingpong */
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#define ULANG 100

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    char *buf = malloc(1 << 24);
    for (int i = 0; i < (1 << 24); i++) buf[i] = (char)i;
    if (rank == 0) printf("%9s %10s %8s\n", "byte", "us", "GB/s");
    for (int n = 1; n <= (1 << 24); n *= 4) {
        MPI_Barrier(MPI_COMM_WORLD);
        double t0 = MPI_Wtime();
        for (int k = 0; k < ULANG; k++) {
            if (rank == 0) {
                MPI_Send(buf, n, MPI_BYTE, 1, 0, MPI_COMM_WORLD);
                MPI_Recv(buf, n, MPI_BYTE, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            } else if (rank == 1) {
                MPI_Recv(buf, n, MPI_BYTE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Send(buf, n, MPI_BYTE, 0, 0, MPI_COMM_WORLD);
            }
        }
        double t = (MPI_Wtime() - t0) / (2.0 * ULANG);
        if (rank == 0) printf("%9d %10.2f %8.3f\n", n, t * 1e6, n / t / 1e9);
    }
    free(buf);
    MPI_Finalize();
    return 0;
}
