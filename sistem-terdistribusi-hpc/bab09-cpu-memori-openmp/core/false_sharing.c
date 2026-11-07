/* Kode 9.10: false sharing. ./false_sharing 0 (buruk) atau 1 (baik)       */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#define T 8
#define ITER 100000000L

struct { volatile long c; } hit[T];                 /* berdempetan */
struct { _Alignas(64) volatile long c; } hit2[T];   /* satu line per penghitung */

int main(int argc, char **argv) {
    int baik = argc > 1 && atoi(argv[1]) == 1;
    double t0 = omp_get_wtime();
    #pragma omp parallel num_threads(T)
    {
        int t = omp_get_thread_num();
        if (baik) for (long i = 0; i < ITER; i++) hit2[t].c++;
        else      for (long i = 0; i < ITER; i++) hit[t].c++;
    }
    printf("%s: %.3f s\n", baik ? "dengan padding" : "false sharing", omp_get_wtime() - t0);
    return 0;
}
