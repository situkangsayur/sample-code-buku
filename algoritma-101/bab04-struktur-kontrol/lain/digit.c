/* Kode 4.4: repeat-until sebagai do-while di C (Algoritma 4.5 BanyakDigit). */
#include <assert.h>
#include <stdio.h>

int banyak_digit(int n) {
    int d = 0;
    do {
        n = n / 10;      /* pembagian bulat untuk int */
        d = d + 1;
    } while (n != 0);    /* syarat lanjut = not (n == 0) */
    return d;
}

int main(void) {
    assert(banyak_digit(2026) == 4);
    assert(banyak_digit(0) == 1);
    printf("digit.c: semua uji lolos\n");
    return 0;
}
