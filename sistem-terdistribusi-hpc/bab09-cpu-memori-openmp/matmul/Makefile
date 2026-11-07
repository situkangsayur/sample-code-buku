# Kode 9.25: perintah praktikum perkalian matriks.
CC ?= gcc
N ?= 2048
all: mm mm_o2
mm: mm.c
	$(CC) -O3 -march=native -fopenmp $< -o $@ -lm
mm_o2: mm.c
	$(CC) -O2 -fopenmp $< -o $@ -lm
cek: mm
	./mm 2 256 --cek && ./mm 4 256 --cek && ./mm 5 256 --cek
bench: all
	OMP_NUM_THREADS=1 ./mm_o2 1 $(N)
	OMP_NUM_THREADS=1 ./mm_o2 2 $(N)
	OMP_NUM_THREADS=1 ./mm 3 $(N)
	OMP_NUM_THREADS=1 ./mm 4 $(N)
	for p in 1 2 4 8; do OMP_NUM_THREADS=$$p OMP_PROC_BIND=close ./mm 5 $(N); done
perf: mm_o2
	perf stat -e cycles,instructions,cache-misses ./mm_o2 1 1024
	perf stat -e cycles,instructions,cache-misses ./mm_o2 2 1024
clean:
	rm -f mm mm_o2
