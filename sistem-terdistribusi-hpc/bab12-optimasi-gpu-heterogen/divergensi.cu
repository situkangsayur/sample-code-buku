// divergensi.cu - membandingkan cabang per-thread (divergen) dengan cabang per-warp.
// Kompilasi: make divergensi ; Jalankan: ./divergensi
#include <cstdio>
#include <cuda_runtime.h>

__device__ float kerjaA(float v) { for (int r = 0; r < 256; ++r) v = v * 1.0001f + 0.1f; return v; }
__device__ float kerjaB(float v) { for (int r = 0; r < 256; ++r) v = v * 0.9999f - 0.1f; return v; }

__global__ void divergen(float *x) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (threadIdx.x % 2 == 0) x[i] = kerjaA(x[i]);   // genap dan ganjil satu warp
  else                      x[i] = kerjaB(x[i]);
}

__global__ void perWarp(float *x) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if ((threadIdx.x / 32) % 2 == 0) x[i] = kerjaA(x[i]);  // satu warp satu cabang
  else                             x[i] = kerjaB(x[i]);
}

int main() {
  int n = 1 << 24;
  float *d; cudaMalloc(&d, n * sizeof(float));
  cudaMemset(d, 0, n * sizeof(float));
  cudaEvent_t a, b; cudaEventCreate(&a); cudaEventCreate(&b);
  for (int v = 0; v < 2; ++v) {
    for (int ulang = 0; ulang < 2; ++ulang) {  // ulang pertama = pemanasan
      cudaEventRecord(a);
      if (v == 0) divergen<<<n / 256, 256>>>(d); else perWarp<<<n / 256, 256>>>(d);
      cudaEventRecord(b); cudaEventSynchronize(b);
    }
    float ms; cudaEventElapsedTime(&ms, a, b);
    printf("%-9s %.3f ms\n", v == 0 ? "divergen" : "per-warp", ms);
  }
  cudaFree(d);
  return 0;
}
