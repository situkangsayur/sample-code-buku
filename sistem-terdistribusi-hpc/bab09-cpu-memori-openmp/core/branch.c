/* Kode 9.7: branch prediction. Bandingkan data acak dan data terurut.
 * make branch && ./branch     (dikompilasi -O1 agar cabang tetap ada)    */
#include <stdio.h>
#include <stdlib.h>
#include "common.h"

static int banding(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

static long dengan_cabang(const int *d, long n) {
    long jumlah = 0;
    for (int r = 0; r < 10; r++)
        for (long i = 0; i < n; i++)
            if (d[i] >= 128) jumlah += d[i];
    return jumlah;
}

static long tanpa_cabang(const int *d, long n) {
    long jumlah = 0;
    for (int r = 0; r < 10; r++)
        for (long i = 0; i < n; i++) {
            int m = -(d[i] >= 128);   /* 0 atau -1 */
            jumlah += d[i] & m;
        }
    return jumlah;
}

int main(void) {
    long n = 32L * 1000 * 1000;
    int *d = malloc(n * sizeof(int));
    srand(42);
    for (long i = 0; i < n; i++) d[i] = rand() % 256;
    double t0 = detik(); long a = dengan_cabang(d, n); double t1 = detik();
    long b = tanpa_cabang(d, n); double t2 = detik();
    qsort(d, n, sizeof(int), banding);
    double t3 = detik(); long c = dengan_cabang(d, n); double t4 = detik();
    printf("acak+cabang   %.3f s\nacak tanpa    %.3f s\nterurut+cabang %.3f s\n",
           t1 - t0, t2 - t1, t4 - t3);
    printf("cek: %ld %ld %ld\n", a, b, c);
    free(d);
    return 0;
}
