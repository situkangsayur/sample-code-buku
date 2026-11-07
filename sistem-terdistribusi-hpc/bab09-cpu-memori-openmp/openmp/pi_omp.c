/* Kode 9.18: menghitung pi dengan parallel for + reduction.
 * for p in 1 2 4 8; do OMP_NUM_THREADS=$p ./pi_omp; done                  */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char **argv) {
    const long N = argc > 1 ? atol(argv[1]) : 1000000000L;
    double h = 1.0 / N, jumlah = 0.0;
    double t0 = omp_get_wtime();
    #pragma omp parallel for reduction(+:jumlah)
    for (long i = 0; i < N; i++) {
        double x = (i + 0.5) * h;
        jumlah += 4.0 / (1.0 + x * x);
    }
    double pi = jumlah * h;
    printf("pi ~ %.12f  %d thread  %.3f s\n", pi, omp_get_max_threads(),
           omp_get_wtime() - t0);
    return 0;
}
