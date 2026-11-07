# Sesuaikan ARCH dengan GPU Anda (lihat nvidia-smi):
#   sm_75 (T4 di Colab), sm_80 (A100), sm_86 (RTX 30xx), sm_89 (L4, RTX 40xx), sm_90 (H100)
ARCH ?= sm_75
NVCC ?= nvcc
FLAGS = -O2 -arch=$(ARCH)

PROGRAM = vadd vadd_ukur stencil1d matmul

all: $(PROGRAM)

%: %.cu
	$(NVCC) $(FLAGS) $< -o $@

# Isian tabel praktikum (Tabel 11.7): vector add dan matmul untuk beberapa ukuran
ukur: vadd_ukur matmul
	@for p in 20 22 24 26; do ./vadd_ukur $$p | tail -1; done
	@for n in 256 512 1024 2048; do ./matmul $$n 16 | tail -1; done
	@for b in 8 16 32; do ./matmul 1024 $$b | tail -1; done

bersih:
	rm -f $(PROGRAM)

.PHONY: all ukur bersih
