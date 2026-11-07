/* Kode 9.17: versi SALAH (race condition). Jalankan beberapa kali: hasil berubah. */
#include <stdio.h>
#include <omp.h>

int main(void) {
    const long N = 100000000L;
    double h = 1.0 / N, jumlah = 0.0;
    #pragma omp parallel for
    for (long i = 0; i < N; i++) {
        double x = (i + 0.5) * h;
        jumlah += 4.0 / (1.0 + x * x);      /* race */
    }
    printf("pi (salah) ~ %.12f\n", jumlah * h);
    return 0;
}
