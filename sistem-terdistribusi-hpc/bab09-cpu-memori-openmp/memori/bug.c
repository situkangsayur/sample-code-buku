/* Kode 9.1: empat bug memori klasik. SENGAJA SALAH, jalankan dengan ASan:
 *   make bug && ./bug     (dikompilasi dengan -fsanitize=address)          */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *buat_nama(void) {
    char *p = malloc(16);
    strcpy(p, "nasabah-0001-xyz");  /* 16 huruf + '\0' = 17: buffer overflow */
    return p;
}

int main(void) {
    char *a = buat_nama();
    free(a);
    printf("%s\n", a);              /* use-after-free */
    free(a);                        /* double free */
    char *b = malloc(1024);         /* tidak pernah di-free: memory leak */
    (void)b;
    return 0;
}
