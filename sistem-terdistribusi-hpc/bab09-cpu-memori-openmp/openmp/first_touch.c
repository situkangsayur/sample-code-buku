/* Kode 9.12: inisialisasi serial vs paralel (first touch, terasa di mesin NUMA). */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

static double jalankan(double *x, long n) {
    double t0 = omp_get_wtime(), s = 0;
    for (int r = 0; r < 10; r++) {
        #pragma omp parallel for schedule(static) reduction(+:s)
        for (long i = 0; i < n; i++) { x[i] = x[i] * 1.000001 + 1.0; s += x[i]; }
    }
    if (s < 0) printf("%f\n", s);
    return omp_get_wtime() - t0;
}

int main(void) {
    long n = 1L << 27;   /* 1 GB */
    double *a = malloc(n * sizeof(double)), *b = malloc(n * sizeof(double));
    for (long i = 0; i < n; i++) a[i] = 0.0;              /* first touch serial */
    #pragma omp parallel for schedule(static)
    for (long i = 0; i < n; i++) b[i] = 0.0;              /* first touch paralel */
    printf("init serial %.3f s, init paralel %.3f s\n", jalankan(a, n), jalankan(b, n));
    free(a); free(b);
    return 0;
}
