#ifndef COMMON_H
#define COMMON_H
#include <time.h>
static inline double detik(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}
#endif
