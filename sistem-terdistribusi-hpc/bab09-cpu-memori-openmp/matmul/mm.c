/* Kode 9.22-9.24: perkalian matriks dari lambat ke cepat.
 * Pemakaian: ./mm <versi 1-5> <n> [--cek]
 *   1 = ijk naif, 2 = ikj, 3 = ikj (kompilasi -O3 -march=native),
 *   4 = ber-blok, 5 = ber-blok + OpenMP
 * Keluaran: versi,n,thread,detik,GFLOPS                                   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>

#define BS 64
#define MIN(a, b) ((a) < (b) ? (a) : (b))

static void mm_ijk(int n, const double *A, const double *B, double *C) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            double s = 0;
            for (int k = 0; k < n; k++)
                s += A[(long)i*n + k] * B[(long)k*n + j];
            C[(long)i*n + j] = s;
        }
}

static void mm_ikj(int n, const double *A, const double *B, double *C) {
    memset(C, 0, (size_t)n * n * sizeof(double));
    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++) {
            double a = A[(long)i*n + k];
            for (int j = 0; j < n; j++)
                C[(long)i*n + j] += a * B[(long)k*n + j];
        }
}

static void blok_kali(int n, int ii, int kk, int jj,
                      const double *A, const double *B, double *C) {
    for (int i = ii; i < MIN(ii + BS, n); i++)
        for (int k = kk; k < MIN(kk + BS, n); k++) {
            double a = A[(long)i*n + k];
            for (int j = jj; j < MIN(jj + BS, n); j++)
                C[(long)i*n + j] += a * B[(long)k*n + j];
        }
}

static void mm_blok(int n, const double *A, const double *B, double *C) {
    memset(C, 0, (size_t)n * n * sizeof(double));
    for (int ii = 0; ii < n; ii += BS)
        for (int kk = 0; kk < n; kk += BS)
            for (int jj = 0; jj < n; jj += BS)
                blok_kali(n, ii, kk, jj, A, B, C);
}

static void mm_blok_omp(int n, const double *A, const double *B, double *C) {
    /* first touch paralel dengan pembagian yang sama */
    #pragma omp parallel for schedule(static)
    for (long i = 0; i < (long)n * n; i++) C[i] = 0.0;
    #pragma omp parallel for schedule(static)
    for (int ii = 0; ii < n; ii += BS)          /* tiap thread memegang baris C sendiri */
        for (int kk = 0; kk < n; kk += BS)
            for (int jj = 0; jj < n; jj += BS)
                blok_kali(n, ii, kk, jj, A, B, C);
}

typedef void (*mm_fn)(int, const double *, const double *, double *);

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "pemakaian: %s <versi 1-5> <n> [--cek]\n", argv[0]); return 1; }
    int v = atoi(argv[1]), n = atoi(argv[2]);
    int cek = argc > 3 && strcmp(argv[3], "--cek") == 0;
    mm_fn fs[] = {NULL, mm_ijk, mm_ikj, mm_ikj, mm_blok, mm_blok_omp};
    if (v < 1 || v > 5) { fprintf(stderr, "versi 1-5\n"); return 1; }
    size_t sz = (size_t)n * n * sizeof(double);
    double *A = malloc(sz), *B = malloc(sz), *C = malloc(sz);
    srand(1);
    for (long i = 0; i < (long)n * n; i++) {
        A[i] = (double)rand() / RAND_MAX;
        B[i] = (double)rand() / RAND_MAX;
    }
    double t0 = omp_get_wtime();
    fs[v](n, A, B, C);
    double t = omp_get_wtime() - t0;
    printf("%d,%d,%d,%.3f,%.2f\n", v, n, v == 5 ? omp_get_max_threads() : 1, t,
           2.0 * n * n * n / t / 1e9);
    if (cek) {
        double *R = malloc(sz), maks = 0;
        mm_ijk(n, A, B, R);
        for (long i = 0; i < (long)n * n; i++) maks = fmax(maks, fabs(R[i] - C[i]));
        printf("selisih maksimum terhadap versi naif: %.3e %s\n", maks,
               maks < 1e-9 ? "(BENAR)" : "(SALAH)");
        free(R);
    }
    free(A); free(B); free(C);
    return 0;
}
