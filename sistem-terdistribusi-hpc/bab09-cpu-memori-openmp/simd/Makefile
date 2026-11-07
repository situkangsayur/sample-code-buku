CC ?= gcc
all: saxpy dot_avx aos_soa
saxpy: saxpy.c
	$(CC) -O3 -march=native $< -o $@
laporan:
	$(CC) -O3 -march=native -fopt-info-vec -c saxpy.c -o /dev/null
dot_avx: dot_avx.c
	$(CC) -O2 -mavx2 -mfma $< -o $@
aos_soa: aos_soa.c
	$(CC) -O3 -march=native $< -o $@
clean:
	rm -f saxpy dot_avx aos_soa
