/* Kode 9.14: dot product dengan intrinsics AVX2 + FMA.
 * Butuh CPU dengan avx2 dan fma (cek: grep -o 'avx2\|fma' /proc/cpuinfo)  */
#include <immintrin.h>
#include <stdio.h>
#include <stdlib.h>

double dot_avx(const double *x, const double *y, long n) {
    __m256d acc = _mm256_setzero_pd();
    long i = 0;
    for (; i + 3 < n; i += 4) {
        __m256d vx = _mm256_loadu_pd(x + i);
        __m256d vy = _mm256_loadu_pd(y + i);
        acc = _mm256_fmadd_pd(vx, vy, acc);      /* acc += vx * vy */
    }
    double t[4];
    _mm256_storeu_pd(t, acc);
    double s = t[0] + t[1] + t[2] + t[3];
    for (; i < n; i++) s += x[i] * y[i];
    return s;
}

double dot_skalar(const double *x, const double *y, long n) {
    double s = 0;
    for (long i = 0; i < n; i++) s += x[i] * y[i];
    return s;
}

int main(void) {
    long n = 1000003;
    double *x = malloc(n * sizeof(double)), *y = malloc(n * sizeof(double));
    for (long i = 0; i < n; i++) { x[i] = 0.5; y[i] = 2.0; }
    printf("avx = %.1f, skalar = %.1f (harus %ld)\n", dot_avx(x, y, n), dot_skalar(x, y, n), n);
    free(x); free(y);
    return 0;
}
