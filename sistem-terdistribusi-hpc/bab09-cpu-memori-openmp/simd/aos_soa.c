/* Kode 9.13: Array of Structures vs Structure of Arrays.                 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 4000000

struct Partikel { float x, y, z, massa; };
struct Partikel2 { float x[N], y[N], z[N], massa[N]; };

static double detik(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

int main(void) {
    struct Partikel *p = calloc(N, sizeof *p);
    struct Partikel2 *q = calloc(1, sizeof *q);
    float *vx = malloc(N * sizeof(float)), dt = 0.01f;
    for (int i = 0; i < N; i++) vx[i] = 1.0f;
    double t0 = detik();
    for (int r = 0; r < 50; r++)
        for (int i = 0; i < N; i++) p[i].x += dt * vx[i];   /* lompat 16 B */
    double t1 = detik();
    for (int r = 0; r < 50; r++)
        for (int i = 0; i < N; i++) q->x[i] += dt * vx[i];  /* stride 1 */
    double t2 = detik();
    printf("AoS %.3f s, SoA %.3f s (cek %.2f %.2f)\n", t1 - t0, t2 - t1, p[7].x, q->x[7]);
    free(p); free(q); free(vx);
    return 0;
}
