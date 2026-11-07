/* Kode 9.6: satu akumulator vs empat akumulator (ILP).
 * make ilp && ./ilp                                                      */
#include <stdio.h>
#include <stdlib.h>
#include "common.h"

double jumlah1(const double *x, long n) {
    double s = 0;
    for (long i = 0; i < n; i++) s += x[i];
    return s;
}

double jumlah4(const double *x, long n) {
    double s0 = 0, s1 = 0, s2 = 0, s3 = 0;
    long i = 0;
    for (; i + 3 < n; i += 4) {
        s0 += x[i];     s1 += x[i + 1];
        s2 += x[i + 2]; s3 += x[i + 3];
    }
    for (; i < n; i++) s0 += x[i];
    return (s0 + s1) + (s2 + s3);
}

int main(void) {
    long n = 1L << 16;                 /* 512 KB: muat di L2, agar tidak memory bound */
    int ulang = 20000;
    double *x = malloc(n * sizeof(double));
    for (long i = 0; i < n; i++) x[i] = 1.0 / (i + 1);
    double s = 0, t0 = detik();
    for (int r = 0; r < ulang; r++) s += jumlah1(x, n);
    double t1 = detik();
    for (int r = 0; r < ulang; r++) s += jumlah4(x, n);
    double t2 = detik();
    printf("1 akumulator: %.3f s, 4 akumulator: %.3f s (cek %.3f)\n", t1 - t0, t2 - t1, s);
    free(x);
    return 0;
}
