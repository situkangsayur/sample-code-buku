MPICC ?= mpicc
CFLAGS ?= -O2
PROG = halo p2p tukar pi jacobi1d pingpong hybrid
all: $(PROG)
hybrid: hybrid.c
	$(MPICC) $(CFLAGS) -fopenmp $< -o $@
%: %.c
	$(MPICC) $(CFLAGS) $< -o $@
scaling: pi
	for np in 1 2 4 8; do mpirun --oversubscribe -np $$np ./pi 1000000000; done
pingpong-tcp: pingpong
	mpirun -np 2 ./pingpong
	mpirun --mca btl self,tcp -np 2 ./pingpong
clean:
	rm -f $(PROG)
