// vadd.cu -- program penjumlahan vektor lengkap (Kode 11.2, 11.6, 11.7).
// Lima langkah: cudaMalloc, salin masuk, kernel, salin keluar, cudaFree.
//
// Kompilasi: nvcc -O2 -arch=sm_75 vadd.cu -o vadd    (sm_75 = T4; lihat Makefile)
// Jalankan : ./vadd
#include <cstdio>
#include <cstdlib>
// Hentikan program bila panggilan CUDA gagal, lengkap dengan lokasinya (Kode 11.6).
// Makro ditulis di setiap berkas agar tiap berkas dapat disalin sendiri ke Colab.
#define CEK(x) do { cudaError_t e = (x); if (e != cudaSuccess) {             \
        fprintf(stderr, "CUDA error: %s di %s:%d\n", cudaGetErrorString(e),  \
                __FILE__, __LINE__);                                          \
        exit(1); } } while (0)

// __global__: dipanggil dari host, dijalankan di device oleh banyak thread
__global__ void tambah(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;   // indeks global thread ini
    if (i < n)                                        // penjaga batas
        c[i] = a[i] + b[i];
}

int main(void) {
    int n = 1 << 24;                                        // 16 juta elemen
    size_t bytes = n * sizeof(float);
    float *a = (float *)malloc(bytes), *b = (float *)malloc(bytes),
          *c = (float *)malloc(bytes);
    if (!a || !b || !c) { fprintf(stderr, "malloc gagal\n"); return 1; }
    for (int i = 0; i < n; i++) { a[i] = 1.0f; b[i] = 2.0f; }

    float *da, *db, *dc;                                    // 1. alokasi
    CEK(cudaMalloc(&da, bytes)); CEK(cudaMalloc(&db, bytes)); CEK(cudaMalloc(&dc, bytes));
    CEK(cudaMemcpy(da, a, bytes, cudaMemcpyHostToDevice));  // 2. salin masuk
    CEK(cudaMemcpy(db, b, bytes, cudaMemcpyHostToDevice));

    int blok = 256, grid = (n + blok - 1) / blok;           // 3. kernel
    tambah<<<grid, blok>>>(da, db, dc, n);
    CEK(cudaGetLastError());                                // error konfigurasi peluncuran
    CEK(cudaDeviceSynchronize());                           // error saat kernel berjalan

    CEK(cudaMemcpy(c, dc, bytes, cudaMemcpyDeviceToHost));  // 4. salin keluar
    printf("c[0] = %.1f, c[n-1] = %.1f\n", c[0], c[n - 1]); // harus 3.0

    // periksa SEMUA elemen, bukan hanya dua
    int salah = 0;
    for (int i = 0; i < n; i++) salah += (c[i] != 3.0f);
    printf("%s: %d elemen salah dari %d\n", salah ? "GAGAL" : "BENAR", salah, n);

    CEK(cudaFree(da)); CEK(cudaFree(db)); CEK(cudaFree(dc)); // 5. bebaskan
    free(a); free(b); free(c);
    return salah ? 1 : 0;
}
