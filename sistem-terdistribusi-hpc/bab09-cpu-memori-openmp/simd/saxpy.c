/* Kode 9.11: saxpy yang mudah di-vectorize.
 * make laporan   -> lihat pesan "loop vectorized"                         */
#include <stdio.h>
#include <stdlib.h>

void saxpy(int n, float a, const float *restrict x, float *restrict y) {
    for (int i = 0; i < n; i++)
        y[i] = a * x[i] + y[i];
}

int main(void) {
    int n = 1 << 24;
    float *x = malloc(n * sizeof(float)), *y = malloc(n * sizeof(float));
    for (int i = 0; i < n; i++) { x[i] = 1.0f; y[i] = 2.0f; }
    saxpy(n, 3.0f, x, y);
    printf("y[0] = %.1f (harus 5.0)\n", y[0]);
    free(x); free(y);
    return 0;
}
