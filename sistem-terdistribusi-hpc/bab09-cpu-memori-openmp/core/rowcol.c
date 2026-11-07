/* Kode 9.9: menjumlahkan matriks per baris vs per kolom.
 * make rowcol && ./rowcol 4096                                           */
#include <stdio.h>
#include <stdlib.h>
#include "common.h"

int main(int argc, char **argv) {
    int N = argc > 1 ? atoi(argv[1]) : 4096;
    double *a = malloc((size_t)N * N * sizeof(double));
    for (long i = 0; i < (long)N * N; i++) a[i] = 1.0;
    double s = 0, t0 = detik();
    for (int i = 0; i < N; i++)            /* per baris: stride 1 */
        for (int j = 0; j < N; j++) s += a[(long)i * N + j];
    double t1 = detik();
    for (int j = 0; j < N; j++)            /* per kolom: stride N */
        for (int i = 0; i < N; i++) s += a[(long)i * N + j];
    double t2 = detik();
    printf("N=%d per baris %.3f s, per kolom %.3f s (cek %.0f)\n", N, t1 - t0, t2 - t1, s);
    free(a);
    return 0;
}
