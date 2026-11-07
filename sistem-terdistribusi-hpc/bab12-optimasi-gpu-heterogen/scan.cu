// scan.cu - exclusive scan (prefix sum) Blelloch untuk satu block berisi 2*BLOK elemen.
// Untuk array besar, hasil per block di-scan lagi lalu ditambahkan (tidak dibahas di sini).
// Kompilasi: make scan ; Jalankan: ./scan
#include <cstdio>
#include <cuda_runtime.h>

#define BLOK 4            // 4 thread menangani 8 elemen; kecil agar mudah dilacak
#define N (2 * BLOK)

__global__ void scanBlelloch(const int *in, int *out) {
  __shared__ int s[N];
  int t = threadIdx.x;
  s[2 * t] = in[2 * t];
  s[2 * t + 1] = in[2 * t + 1];
  // Fase naik (up-sweep / reduce)
  int offset = 1;
  for (int d = N >> 1; d > 0; d >>= 1) {
    __syncthreads();
    if (t < d) {
      int ai = offset * (2 * t + 1) - 1;
      int bi = offset * (2 * t + 2) - 1;
      s[bi] += s[ai];
    }
    offset <<= 1;
  }
  if (t == 0) s[N - 1] = 0;     // akar diganti identitas penjumlahan
  // Fase turun (down-sweep)
  for (int d = 1; d < N; d <<= 1) {
    offset >>= 1;
    __syncthreads();
    if (t < d) {
      int ai = offset * (2 * t + 1) - 1;
      int bi = offset * (2 * t + 2) - 1;
      int tmp = s[ai];
      s[ai] = s[bi];
      s[bi] += tmp;
    }
  }
  __syncthreads();
  out[2 * t] = s[2 * t];
  out[2 * t + 1] = s[2 * t + 1];
}

int main() {
  int h[N] = {3, 1, 7, 0, 4, 1, 6, 3}, hasil[N];
  int *dIn, *dOut;
  cudaMalloc(&dIn, sizeof(h)); cudaMalloc(&dOut, sizeof(h));
  cudaMemcpy(dIn, h, sizeof(h), cudaMemcpyHostToDevice);
  scanBlelloch<<<1, BLOK>>>(dIn, dOut);
  cudaMemcpy(hasil, dOut, sizeof(h), cudaMemcpyDeviceToHost);
  printf("exclusive scan:");
  for (int i = 0; i < N; ++i) printf(" %d", hasil[i]);   // 0 3 4 11 11 15 16 22
  printf("\n");
  cudaFree(dIn); cudaFree(dOut);
  return 0;
}
