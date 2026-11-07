/* Kode 9.19: bilangan prima dengan schedule(runtime).
 * OMP_SCHEDULE="static"       ./prima_omp
 * OMP_SCHEDULE="dynamic,1000" ./prima_omp                                */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char **argv) {
    long N = argc > 1 ? atol(argv[1]) : 20000000L;
    long total = 0;
    double t0 = omp_get_wtime();
    #pragma omp parallel for schedule(runtime) reduction(+:total)
    for (long n = 2; n < N; n++) {
        int prima = 1;
        for (long d = 2; d * d <= n; d++)
            if (n % d == 0) { prima = 0; break; }
        total += prima;
    }
    printf("%ld prima di bawah %ld, %d thread, %.3f s\n", total, N,
           omp_get_max_threads(), omp_get_wtime() - t0);
    return 0;
}
