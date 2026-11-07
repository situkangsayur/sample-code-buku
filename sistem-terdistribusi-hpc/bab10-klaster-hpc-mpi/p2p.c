/* Kode 10.4: rank 0 mengirim 100 double ke rank 1.  mpirun -np 2 ./p2p */
#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if (size < 2) { if (rank == 0) printf("butuh minimal 2 proses\n"); MPI_Finalize(); return 1; }
    double data[100];
    if (rank == 0) {
        for (int i = 0; i < 100; i++) data[i] = i * 0.5;
        MPI_Send(data, 100, MPI_DOUBLE, 1, 7, MPI_COMM_WORLD);
    } else if (rank == 1) {
        MPI_Status st;
        MPI_Recv(data, 100, MPI_DOUBLE, 0, 7, MPI_COMM_WORLD, &st);
        int n;
        MPI_Get_count(&st, MPI_DOUBLE, &n);
        printf("rank 1 menerima %d elemen dari rank %d (tag %d), data[99] = %.1f\n",
               n, st.MPI_SOURCE, st.MPI_TAG, data[99]);
    }
    MPI_Finalize();
    return 0;
}
