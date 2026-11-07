/* Kode 9.15: program OpenMP pertama. OMP_NUM_THREADS=4 ./halo             */
#include <stdio.h>
#include <omp.h>

int main(void) {
    #pragma omp parallel
    {
        int id = omp_get_thread_num();
        int n  = omp_get_num_threads();
        printf("halo dari thread %d dari %d\n", id, n);
    }
    return 0;
}
