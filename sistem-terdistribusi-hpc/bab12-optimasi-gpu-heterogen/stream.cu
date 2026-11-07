// stream.cu - menumpuk transfer dan komputasi dengan beberapa CUDA stream.
// Bandingkan waktu 1 stream (serial) dengan K stream.
// Kompilasi: make stream ; Jalankan: ./stream 4
#include <cstdio>
#include <cstdlib>
#include <cuda_runtime.h>

__global__ void skala(float *x, int n, float a) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n) {
    float v = x[i];
    for (int r = 0; r < 200; ++r) v = v * a + 0.5f;   // beban hitung buatan
    x[i] = v;
  }
}

float jalankan(float *h, float *d, int n, int K) {
  cudaStream_t s[16];
  for (int k = 0; k < K; ++k) cudaStreamCreate(&s[k]);
  int potong = n / K;
  cudaEvent_t a, b; cudaEventCreate(&a); cudaEventCreate(&b);
  cudaEventRecord(a);
  for (int k = 0; k < K; ++k) {
    int off = k * potong;
    size_t bytes = potong * sizeof(float);
    // tiga langkah tiap potongan masuk ke stream yang sama: urut di dalam stream,
    // tetapi boleh tumpang tindih dengan stream lain
    cudaMemcpyAsync(d + off, h + off, bytes, cudaMemcpyHostToDevice, s[k]);
    skala<<<(potong + 255) / 256, 256, 0, s[k]>>>(d + off, potong, 0.999f);
    cudaMemcpyAsync(h + off, d + off, bytes, cudaMemcpyDeviceToHost, s[k]);
  }
  cudaEventRecord(b); cudaEventSynchronize(b);
  float ms; cudaEventElapsedTime(&ms, a, b);
  for (int k = 0; k < K; ++k) cudaStreamDestroy(s[k]);
  return ms;
}

int main(int argc, char **argv) {
  int K = (argc > 1) ? atoi(argv[1]) : 4;
  if (K < 1 || K > 16) K = 4;
  int n = 1 << 26;                       // 64 Mi float = 256 MB
  float *h, *d;
  cudaMallocHost(&h, n * sizeof(float)); // pinned memory: syarat copy asinkron sungguhan
  cudaMalloc(&d, n * sizeof(float));
  for (int i = 0; i < n; ++i) h[i] = 1.0f;
  jalankan(h, d, n, 1);                  // pemanasan
  printf("1 stream : %.2f ms\n", jalankan(h, d, n, 1));
  printf("%d stream : %.2f ms\n", K, jalankan(h, d, n, K));
  cudaFreeHost(h); cudaFree(d);
  return 0;
}
