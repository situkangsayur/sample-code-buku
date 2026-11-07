# Sesuaikan ARCH dengan GPU Anda: sm_75 (T4), sm_80 (A100), sm_86 (RTX 30xx), sm_89 (L4, RTX 40xx).
ARCH ?= sm_75
NVCC ?= nvcc
FLAGS = -O3 -arch=$(ARCH)

all: matmul reduksi histogram scan stream divergensi

matmul: matmul.cu
	$(NVCC) $(FLAGS) $< -o $@ -lcublas
matmul16 matmul32: matmul.cu
	$(NVCC) $(FLAGS) -DTILE=$(subst matmul,,$@) $< -o $@ -lcublas
%: %.cu
	$(NVCC) $(FLAGS) $< -o $@

# Laporan register dan shared memory per kernel (bahan menghitung occupancy)
info: matmul.cu
	$(NVCC) $(FLAGS) -Xptxas -v -c $< -o /dev/null

bersih:
	rm -f matmul matmul16 matmul32 reduksi histogram scan stream divergensi
.PHONY: all info bersih
