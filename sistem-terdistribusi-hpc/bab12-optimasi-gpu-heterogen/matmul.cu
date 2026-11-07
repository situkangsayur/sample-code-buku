// matmul.cu - perkalian matriks C = A * B di GPU dalam tiga versi:
//   1) naif (satu thread satu elemen, langsung dari global memory)
//   2) tiled dengan shared memory (TILE x TILE)
//   3) cuBLAS (pembanding produksi)
// Setiap versi diukur dengan cudaEvent (pemanasan + median 5 kali),
// dicetak dalam ms dan GFLOPS, lalu diverifikasi terhadap cuBLAS.
//
// Kompilasi : make matmul        (atau: nvcc -O3 -arch=sm_75 matmul.cu -o matmul -lcublas)
// Jalankan  : ./matmul 2048
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <algorithm>
#include <cuda_runtime.h>
#include <cublas_v2.h>

#ifndef TILE
#define TILE 16
#endif

#define CEK(x) do { cudaError_t e = (x); if (e != cudaSuccess) { \
  fprintf(stderr, "CUDA error %s di %s:%d\n", cudaGetErrorString(e), __FILE__, __LINE__); \
  exit(1); } } while (0)

// Versi naif: threadIdx.x dipetakan ke kolom agar akses B dan C coalesced.
__global__ void matmulNaif(const float *A, const float *B, float *C, int N) {
  int row = blockIdx.y * blockDim.y + threadIdx.y;
  int col = blockIdx.x * blockDim.x + threadIdx.x;
  if (row < N && col < N) {
    float acc = 0.0f;
    for (int k = 0; k < N; ++k) acc += A[row * N + k] * B[k * N + col];
    C[row * N + col] = acc;
  }
}

// Versi tiled: satu block TILE x TILE memuat tile A dan tile B ke shared memory.
__global__ void matmulTiled(const float *A, const float *B, float *C, int N) {
  __shared__ float As[TILE][TILE];
  __shared__ float Bs[TILE][TILE];
  int row = blockIdx.y * TILE + threadIdx.y;
  int col = blockIdx.x * TILE + threadIdx.x;
  float acc = 0.0f;
  for (int t = 0; t < (N + TILE - 1) / TILE; ++t) {
    int aCol = t * TILE + threadIdx.x;
    int bRow = t * TILE + threadIdx.y;
    As[threadIdx.y][threadIdx.x] = (row < N && aCol < N) ? A[row * N + aCol] : 0.0f;
    Bs[threadIdx.y][threadIdx.x] = (bRow < N && col < N) ? B[bRow * N + col] : 0.0f;
    __syncthreads();                 // tile lengkap sebelum dipakai
    for (int k = 0; k < TILE; ++k) acc += As[threadIdx.y][k] * Bs[k][threadIdx.x];
    __syncthreads();                 // tile lama selesai dipakai sebelum ditimpa
  }
  if (row < N && col < N) C[row * N + col] = acc;
}

// Mengukur satu peluncuran: pemanasan sekali, lalu median dari 5 kali.
template <typename F>
float ukur(F jalankan) {
  cudaEvent_t mulai, selesai;
  CEK(cudaEventCreate(&mulai));
  CEK(cudaEventCreate(&selesai));
  jalankan();                         // pemanasan
  CEK(cudaDeviceSynchronize());
  std::vector<float> t;
  for (int r = 0; r < 5; ++r) {
    CEK(cudaEventRecord(mulai));
    jalankan();
    CEK(cudaEventRecord(selesai));
    CEK(cudaEventSynchronize(selesai)); // tanpa ini yang terukur hanya waktu antre
    float ms = 0.0f;
    CEK(cudaEventElapsedTime(&ms, mulai, selesai));
    t.push_back(ms);
  }
  std::sort(t.begin(), t.end());
  cudaEventDestroy(mulai);
  cudaEventDestroy(selesai);
  return t[t.size() / 2];
}

double selisihRelatif(const std::vector<float> &x, const std::vector<float> &acuan) {
  double num = 0.0, den = 0.0;
  for (size_t i = 0; i < x.size(); ++i) {
    double d = (double)x[i] - acuan[i];
    num += d * d;
    den += (double)acuan[i] * acuan[i];
  }
  return std::sqrt(num / den);
}

int main(int argc, char **argv) {
  int N = (argc > 1) ? atoi(argv[1]) : 1024;
  size_t bytes = (size_t)N * N * sizeof(float);
  std::vector<float> hA((size_t)N * N), hB((size_t)N * N), hC((size_t)N * N), hRef((size_t)N * N);
  srand(42);
  for (auto &v : hA) v = (float)rand() / RAND_MAX - 0.5f;
  for (auto &v : hB) v = (float)rand() / RAND_MAX - 0.5f;

  float *dA, *dB, *dC;
  CEK(cudaMalloc(&dA, bytes)); CEK(cudaMalloc(&dB, bytes)); CEK(cudaMalloc(&dC, bytes));
  CEK(cudaMemcpy(dA, hA.data(), bytes, cudaMemcpyHostToDevice));
  CEK(cudaMemcpy(dB, hB.data(), bytes, cudaMemcpyHostToDevice));

  dim3 blk(TILE, TILE);
  dim3 grd((N + TILE - 1) / TILE, (N + TILE - 1) / TILE);
  double flop = 2.0 * N * (double)N * N;

  // cuBLAS sebagai acuan kebenaran. cuBLAS column-major: hitung C^T = B^T A^T.
  cublasHandle_t h;
  cublasCreate(&h);
  const float alpha = 1.0f, beta = 0.0f;
  auto jalanCublas = [&]() {
    cublasSgemm(h, CUBLAS_OP_N, CUBLAS_OP_N, N, N, N, &alpha, dB, N, dA, N, &beta, dC, N);
  };
  float msCublas = ukur(jalanCublas);
  CEK(cudaMemcpy(hRef.data(), dC, bytes, cudaMemcpyDeviceToHost));

  float msNaif = ukur([&]() { matmulNaif<<<grd, blk>>>(dA, dB, dC, N); });
  CEK(cudaGetLastError());
  CEK(cudaMemcpy(hC.data(), dC, bytes, cudaMemcpyDeviceToHost));
  double errNaif = selisihRelatif(hC, hRef);

  float msTiled = ukur([&]() { matmulTiled<<<grd, blk>>>(dA, dB, dC, N); });
  CEK(cudaGetLastError());
  CEK(cudaMemcpy(hC.data(), dC, bytes, cudaMemcpyDeviceToHost));
  double errTiled = selisihRelatif(hC, hRef);

  printf("versi,N,TILE,ms,GFLOPS,galat_relatif\n");
  printf("naif,%d,%d,%.3f,%.1f,%.2e\n", N, TILE, msNaif, flop / (msNaif * 1e6), errNaif);
  printf("tiled,%d,%d,%.3f,%.1f,%.2e\n", N, TILE, msTiled, flop / (msTiled * 1e6), errTiled);
  printf("cublas,%d,-,%.3f,%.1f,0\n", N, msCublas, flop / (msCublas * 1e6));

  cublasDestroy(h);
  cudaFree(dA); cudaFree(dB); cudaFree(dC);
  return (errNaif < 1e-4 && errTiled < 1e-4) ? 0 : 2;
}
