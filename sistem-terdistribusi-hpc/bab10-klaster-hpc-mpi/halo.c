/* Kode 10.1: program MPI pertama.  mpicc -O2 halo.c -o halo && mpirun -np 4 ./halo */
#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size, len;
    char nama[MPI_MAX_PROCESSOR_NAME];
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Get_processor_name(nama, &len);
    printf("Halo dari rank %d dari %d, di %s\n", rank, size, nama);
    MPI_Finalize();
    return 0;
}
