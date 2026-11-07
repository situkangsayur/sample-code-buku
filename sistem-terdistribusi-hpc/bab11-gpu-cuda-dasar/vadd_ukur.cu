// vadd_ukur.cu -- mengukur penjumlahan vektor dengan cudaEvent (Kode 11.12):
// waktu CPU, salin masuk, kernel, salin keluar, dan total, untuk mengisi
// tabel praktikum (Tabel 11.7). Waktu kernel = median beberapa ulangan
// setelah pemanasan.
//
// Kompilasi: nvcc -O2 -arch=sm_75 vadd_ukur.cu -o vadd_ukur
// Jalankan : ./vadd_ukur 24        (n = 2^24; default 24)
//            ./vadd_ukur 26 pinned (memakai pinned memory, cudaMallocHost)
// Keluaran : baris CSV  n,cpu_ms,h2d_ms,kernel_ms,d2h_ms,gpu_total_ms,kernel_GBs,speedup_kernel,speedup_total
#include <algorithm>
#include <chrono>
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

__global__ void tambah(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
        c[i] = a[i] + b[i];
}

// versi CPU satu thread sebagai pembanding dan pemeriksa kebenaran
static void tambah_cpu(const float *a, const float *b, float *c, int n) {
    for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
}

int main(int argc, char **argv) {
    int pangkat = argc > 1 ? atoi(argv[1]) : 24;
    bool pinned = argc > 2 && strcmp(argv[2], "pinned") == 0;
    if (pangkat < 10 || pangkat > 29) { fprintf(stderr, "pangkat 10..29\n"); return 1; }
    int n = 1 << pangkat;
    size_t bytes = (size_t)n * sizeof(float);

    float *a, *b, *c, *ref;
    if (pinned) {                       // memori host terkunci: DMA langsung
        CEK(cudaMallocHost(&a, bytes)); CEK(cudaMallocHost(&b, bytes)); CEK(cudaMallocHost(&c, bytes));
    } else {
        a = (float *)malloc(bytes); b = (float *)malloc(bytes); c = (float *)malloc(bytes);
    }
    ref = (float *)malloc(bytes);
    if (!a || !b || !c || !ref) { fprintf(stderr, "alokasi host gagal\n"); return 1; }
    for (int i = 0; i < n; i++) { a[i] = (float)(i % 1000); b[i] = 0.5f * (i % 7); }
    memset(c, 0, bytes);                // sentuh halaman c lebih dulu agar salin keluar
    memset(ref, 0, bytes);              // tidak ikut menanggung biaya page fault pertama

    // CPU: median dari 3 ulangan
    std::vector<double> tcpu;
    for (int r = 0; r < 3; r++) {
        auto t0 = std::chrono::steady_clock::now();
        tambah_cpu(a, b, ref, n);
        auto t1 = std::chrono::steady_clock::now();
        tcpu.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());
    }
    std::sort(tcpu.begin(), tcpu.end());
    double cpu_ms = tcpu[1];

    float *da, *db, *dc;
    CEK(cudaMalloc(&da, bytes)); CEK(cudaMalloc(&db, bytes)); CEK(cudaMalloc(&dc, bytes));
    int blok = 256, grid = (n + blok - 1) / blok;

    cudaEvent_t mulai, selesai;
    CEK(cudaEventCreate(&mulai));
    CEK(cudaEventCreate(&selesai));
    float ms = 0.0f;

    // pemanasan: konteks CUDA, kode kernel, alokasi pertama (tidak diukur)
    tambah<<<grid, blok>>>(da, db, dc, n);
    CEK(cudaGetLastError());
    CEK(cudaDeviceSynchronize());

    // salin masuk (host ke device)
    CEK(cudaEventRecord(mulai));
    CEK(cudaMemcpy(da, a, bytes, cudaMemcpyHostToDevice));
    CEK(cudaMemcpy(db, b, bytes, cudaMemcpyHostToDevice));
    CEK(cudaEventRecord(selesai));
    CEK(cudaEventSynchronize(selesai));
    CEK(cudaEventElapsedTime(&ms, mulai, selesai));
    float h2d_ms = ms;

    // kernel: median dari 11 ulangan
    std::vector<float> tk;
    for (int r = 0; r < 11; r++) {
        CEK(cudaEventRecord(mulai));
        tambah<<<grid, blok>>>(da, db, dc, n);
        CEK(cudaEventRecord(selesai));
        CEK(cudaEventSynchronize(selesai));               // tunggu event selesai
        CEK(cudaGetLastError());
        CEK(cudaEventElapsedTime(&ms, mulai, selesai));
        tk.push_back(ms);
    }
    std::sort(tk.begin(), tk.end());
    float kernel_ms = tk[tk.size() / 2];

    // salin keluar (device ke host)
    CEK(cudaEventRecord(mulai));
    CEK(cudaMemcpy(c, dc, bytes, cudaMemcpyDeviceToHost));
    CEK(cudaEventRecord(selesai));
    CEK(cudaEventSynchronize(selesai));
    CEK(cudaEventElapsedTime(&ms, mulai, selesai));
    float d2h_ms = ms;

    int salah = 0;
    for (int i = 0; i < n; i++) salah += (c[i] != ref[i]);
    float total_ms = h2d_ms + kernel_ms + d2h_ms;
    double gbs = 3.0 * bytes / kernel_ms / 1e6;          // baca a, b, tulis c

    fprintf(stderr, "n = 2^%d (%s), %s; kernel: %.3f ms, bandwidth efektif: %.1f GB/s\n",
            pangkat, pinned ? "pinned" : "pageable", salah ? "HASIL SALAH" : "hasil benar",
            kernel_ms, gbs);
    printf("n,cpu_ms,h2d_ms,kernel_ms,d2h_ms,gpu_total_ms,kernel_GBs,speedup_kernel,speedup_total\n");
    printf("%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.1f,%.2f,%.2f\n", n, cpu_ms, h2d_ms, kernel_ms, d2h_ms,
           total_ms, gbs, cpu_ms / kernel_ms, cpu_ms / total_ms);

    CEK(cudaEventDestroy(mulai)); CEK(cudaEventDestroy(selesai));
    CEK(cudaFree(da)); CEK(cudaFree(db)); CEK(cudaFree(dc));
    if (pinned) { CEK(cudaFreeHost(a)); CEK(cudaFreeHost(b)); CEK(cudaFreeHost(c)); }
    else { free(a); free(b); free(c); }
    free(ref);
    return salah ? 1 : 0;
}
