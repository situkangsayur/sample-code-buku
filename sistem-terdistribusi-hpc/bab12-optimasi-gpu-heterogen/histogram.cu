// histogram.cu - histogram 256 bin dengan privatization di shared memory.
// Kompilasi: make histogram ; Jalankan: ./histogram 100000000
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cuda_runtime.h>

__global__ void histoNaif(const unsigned char *data, int n, unsigned int *bins) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += blockDim.x * gridDim.x)
    atomicAdd(&bins[data[i]], 1u);      // semua block antre di global memory
}

__global__ void histoPrivat(const unsigned char *data, int n, unsigned int *bins) {
  __shared__ unsigned int lokal[256];
  for (int b = threadIdx.x; b < 256; b += blockDim.x) lokal[b] = 0;
  __syncthreads();
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += blockDim.x * gridDim.x)
    atomicAdd(&lokal[data[i]], 1u);     // antre di shared memory yang cepat
  __syncthreads();
  for (int b = threadIdx.x; b < 256; b += blockDim.x) atomicAdd(&bins[b], lokal[b]);
}

int main(int argc, char **argv) {
  int n = (argc > 1) ? atoi(argv[1]) : 100000000;
  std::vector<unsigned char> h(n);
  srand(1);
  for (int i = 0; i < n; ++i) h[i] = (unsigned char)(rand() & 0xFF);
  std::vector<unsigned int> acuan(256, 0), hasil(256);
  for (int i = 0; i < n; ++i) acuan[h[i]]++;

  unsigned char *dData; unsigned int *dBins;
  cudaMalloc(&dData, n); cudaMalloc(&dBins, 256 * sizeof(unsigned int));
  cudaMemcpy(dData, h.data(), n, cudaMemcpyHostToDevice);

  cudaEvent_t a, b; cudaEventCreate(&a); cudaEventCreate(&b);
  const char *nama[2] = {"naif", "privatisasi"};
  for (int v = 0; v < 2; ++v) {
    cudaMemset(dBins, 0, 256 * sizeof(unsigned int));
    cudaEventRecord(a);
    if (v == 0) histoNaif<<<1024, 256>>>(dData, n, dBins);
    else        histoPrivat<<<1024, 256>>>(dData, n, dBins);
    cudaEventRecord(b); cudaEventSynchronize(b);
    float ms; cudaEventElapsedTime(&ms, a, b);
    cudaMemcpy(hasil.data(), dBins, 256 * sizeof(unsigned int), cudaMemcpyDeviceToHost);
    bool benar = (hasil == acuan);
    printf("%-12s %8.3f ms  %s\n", nama[v], ms, benar ? "LULUS" : "GAGAL");
  }
  cudaFree(dData); cudaFree(dBins);
  return 0;
}
