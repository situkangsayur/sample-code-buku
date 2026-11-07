// matmul.cu -- perkalian matriks naif: satu thread per elemen C (Kode 11.11).
// Mengukur waktu kernel dengan cudaEvent, menghitung GFLOPS = 2 n^3 / t,
// memeriksa hasil terhadap CPU, dan menerima ukuran block sebagai argumen
// untuk percobaan 8x8, 16x16, 32x32 (dan 64x64 yang gagal diluncurkan).
//
// Kompilasi: nvcc -O2 -arch=sm_75 matmul.cu -o matmul
// Jalankan : ./matmul 1024          (n = 1024, block 16x16)
//            ./matmul 1024 32       (block 32x32)
//            ./matmul 512 64        (block 64x64 = 4096 thread: gagal, dan terdeteksi)
//            ./matmul 2048 16 cpu   (paksa pembanding CPU penuh; lambat untuk n besar)
// Keluaran : baris CSV  n,blok,cpu_ms,h2d_ms,kernel_ms,d2h_ms,gpu_total_ms,GFLOPS,galat_relatif
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

// Hentikan program bila panggilan CUDA gagal, lengkap dengan lokasinya (Kode 11.6).
// Makro ditulis di setiap berkas agar tiap berkas dapat disalin sendiri ke Colab.
#define CEK(x) do { cudaError_t e = (x); if (e != cudaSuccess) {             \
        fprintf(stderr, "CUDA error: %s di %s:%d\n", cudaGetErrorString(e),  \
                __FILE__, __LINE__);                                          \
        exit(1); } } while (0)

// C = A x B, semua matriks n x n, float, row-major
__global__ void matmul(const float *A, const float *B, float *C, int n) {
    int baris = blockIdx.y * blockDim.y + threadIdx.y;
    int kolom = blockIdx.x * blockDim.x + threadIdx.x;
    if (baris < n && kolom < n) {
        float jumlah = 0.0f;
        for (int k = 0; k < n; k++)
            jumlah += A[baris * n + k] * B[k * n + kolom];
        C[baris * n + kolom] = jumlah;
    }
}

// pembanding CPU satu thread, urutan loop i-k-j agar ramah cache (Bab 9)
static void matmul_cpu(const float *A, const float *B, float *C, int n) {
    memset(C, 0, (size_t)n * n * sizeof(float));
    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++) {
            float a = A[(size_t)i * n + k];
            for (int j = 0; j < n; j++) C[(size_t)i * n + j] += a * B[(size_t)k * n + j];
        }
}

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 1024;
    int b = argc > 2 ? atoi(argv[2]) : 16;
    bool cpu_penuh = (argc > 3 && strcmp(argv[3], "cpu") == 0) || n <= 1024;
    size_t bytes = (size_t)n * n * sizeof(float);

    float *A = (float *)malloc(bytes), *B = (float *)malloc(bytes), *C = (float *)malloc(bytes);
    for (size_t i = 0; i < (size_t)n * n; i++) {
        A[i] = (float)((i * 7) % 13) / 13.0f - 0.5f;
        B[i] = (float)((i * 11) % 17) / 17.0f - 0.5f;
    }

    float *dA, *dB, *dC;
    CEK(cudaMalloc(&dA, bytes)); CEK(cudaMalloc(&dB, bytes)); CEK(cudaMalloc(&dC, bytes));
    cudaEvent_t e0, e1;
    CEK(cudaEventCreate(&e0)); CEK(cudaEventCreate(&e1));
    float h2d_ms, kernel_ms, d2h_ms;

    CEK(cudaEventRecord(e0));
    CEK(cudaMemcpy(dA, A, bytes, cudaMemcpyHostToDevice));
    CEK(cudaMemcpy(dB, B, bytes, cudaMemcpyHostToDevice));
    CEK(cudaEventRecord(e1));
    CEK(cudaEventSynchronize(e1));
    CEK(cudaEventElapsedTime(&h2d_ms, e0, e1));

    // peluncuran
    dim3 blok(b, b);
    dim3 grid((n + b - 1) / b, (n + b - 1) / b);
    matmul<<<grid, blok>>>(dA, dB, dC, n);               // pemanasan
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        // contoh: block 64x64 = 4096 thread melebihi batas 1024 thread per block
        fprintf(stderr, "peluncuran gagal (block %dx%d = %d thread): %s\n",
                b, b, b * b, cudaGetErrorString(err));
        return 1;
    }
    CEK(cudaDeviceSynchronize());

    std::vector<float> tk;
    for (int r = 0; r < 5; r++) {
        CEK(cudaEventRecord(e0));
        matmul<<<grid, blok>>>(dA, dB, dC, n);
        CEK(cudaEventRecord(e1));
        CEK(cudaEventSynchronize(e1));
        float ms; CEK(cudaEventElapsedTime(&ms, e0, e1));
        tk.push_back(ms);
    }
    std::sort(tk.begin(), tk.end());
    kernel_ms = tk[tk.size() / 2];                         // median

    CEK(cudaEventRecord(e0));
    CEK(cudaMemcpy(C, dC, bytes, cudaMemcpyDeviceToHost));
    CEK(cudaEventRecord(e1));
    CEK(cudaEventSynchronize(e1));
    CEK(cudaEventElapsedTime(&d2h_ms, e0, e1));

    // Periksa kebenaran. Untuk n besar, CPU penuh sangat lambat (n^3), jadi cukup
    // periksa 256 elemen acak dengan perkalian titik langsung.
    double cpu_ms = -1, galat = 0, norma = 0;
    if (cpu_penuh) {
        float *ref = (float *)malloc(bytes);
        auto t0 = std::chrono::steady_clock::now();
        matmul_cpu(A, B, ref, n);
        auto t1 = std::chrono::steady_clock::now();
        cpu_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        for (size_t i = 0; i < (size_t)n * n; i++) {
            galat = fmax(galat, fabs((double)C[i] - ref[i]));
            norma = fmax(norma, fabs((double)ref[i]));
        }
        free(ref);
    } else {
        srand(1);
        for (int s = 0; s < 256; s++) {
            int i = rand() % n, j = rand() % n;
            double r = 0;
            for (int k = 0; k < n; k++) r += (double)A[(size_t)i * n + k] * B[(size_t)k * n + j];
            galat = fmax(galat, fabs((double)C[(size_t)i * n + j] - r));
            norma = fmax(norma, fabs(r));
        }
    }
    double galat_rel = galat / fmax(norma, 1e-30);
    double gflops = 2.0 * n * (double)n * n / (kernel_ms * 1e6);
    float total_ms = h2d_ms + kernel_ms + d2h_ms;

    fprintf(stderr, "matmul naif n=%d block %dx%d: kernel %.3f ms, %.1f GFLOPS, galat relatif %.2e (%s)\n",
            n, b, b, kernel_ms, gflops, galat_rel, galat_rel < 1e-4 ? "benar" : "PERIKSA");
    printf("n,blok,cpu_ms,h2d_ms,kernel_ms,d2h_ms,gpu_total_ms,GFLOPS,galat_relatif\n");
    printf("%d,%d,%.1f,%.3f,%.3f,%.3f,%.3f,%.1f,%.2e\n", n, b, cpu_ms, h2d_ms, kernel_ms, d2h_ms,
           total_ms, gflops, galat_rel);

    CEK(cudaFree(dA)); CEK(cudaFree(dB)); CEK(cudaFree(dC));
    free(A); free(B); free(C);
    return galat_rel < 1e-4 ? 0 : 1;
}
