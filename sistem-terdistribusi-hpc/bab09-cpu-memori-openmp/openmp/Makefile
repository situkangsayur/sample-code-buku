CC ?= gcc
CFLAGS ?= -O2 -fopenmp
PROG = halo pi_salah pi_omp prima_omp first_touch
all: $(PROG)
%: %.c
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm -f $(PROG)
