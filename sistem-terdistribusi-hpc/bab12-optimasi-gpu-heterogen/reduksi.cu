// reduksi.cu - menjumlahkan n bilangan dengan reduction pohon di shared memory.
// Kompilasi: make reduksi ; Jalankan: ./reduksi 16777216
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <cuda_runtime.h>

#define BLOK 256   // harus pangkat dua

__global__ void reduceSum(const float *in, float *out, int n) {
  __shared__ float s[BLOK];
  int tid = threadIdx.x;
  int i = blockIdx.x * blockDim.x + tid;
  s[tid] = (i < n) ? in[i] : 0.0f;
  __syncthreads();
  // stride menyusut separuh: thread aktif selalu 0..stride-1 (sedikit divergence)
  for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
    if (tid < stride) s[tid] += s[tid + stride];
    __syncthreads();
  }
  if (tid == 0) atomicAdd(out, s[0]);   // gabungkan hasil antar-block
}

int main(int argc, char **argv) {
  int n = (argc > 1) ? atoi(argv[1]) : (1 << 24);
  std::vector<float> h(n, 1.0f);       // semua 1, jadi jawabannya n
  float *dIn, *dOut, hasil = 0.0f;
  cudaMalloc(&dIn, n * sizeof(float));
  cudaMalloc(&dOut, sizeof(float));
  cudaMemcpy(dIn, h.data(), n * sizeof(float), cudaMemcpyHostToDevice);
  cudaMemset(dOut, 0, sizeof(float));
  reduceSum<<<(n + BLOK - 1) / BLOK, BLOK>>>(dIn, dOut, n);
  cudaMemcpy(&hasil, dOut, sizeof(float), cudaMemcpyDeviceToHost);
  printf("jumlah = %.0f (harapan %d)\n", hasil, n);
  cudaFree(dIn); cudaFree(dOut);
  // FP32 hanya tepat untuk bilangan bulat sampai 2^24; untuk n lebih besar
  // hasil bisa sedikit meleset: contoh nyata bahwa penjumlahan float tidak asosiatif.
  return 0;
}
