// stencil1d.cu -- stencil 1D radius R = 3 dengan shared memory dan
// __syncthreads (Kode 11.5), dibandingkan versi tanpa shared memory dan versi CPU.
//
// Kompilasi: nvcc -O2 -arch=sm_75 stencil1d.cu -o stencil1d
// Jalankan : ./stencil1d          (n = 2^24 + 5, sengaja bukan kelipatan BLOK)
//            ./stencil1d 1000
#include <cmath>
#include <cstdio>
#include <cstdlib>

// Hentikan program bila panggilan CUDA gagal, lengkap dengan lokasinya (Kode 11.6).
// Makro ditulis di setiap berkas agar tiap berkas dapat disalin sendiri ke Colab.
#define CEK(x) do { cudaError_t e = (x); if (e != cudaSuccess) {             \
        fprintf(stderr, "CUDA error: %s di %s:%d\n", cudaGetErrorString(e),  \
                __FILE__, __LINE__);                                          \
        exit(1); } } while (0)

#define R 3
#define BLOK 256

__global__ void stencil1d(const float *in, float *out, int n) {
    __shared__ float tmp[BLOK + 2 * R];          // dibagi semua thread satu block
    int g = blockIdx.x * blockDim.x + threadIdx.x;  // indeks global
    int l = threadIdx.x + R;                         // indeks lokal di tmp
    tmp[l] = (g < n) ? in[g] : 0.0f;
    if (threadIdx.x < R) {                           // R thread pertama memuat halo
        tmp[l - R]    = (g - R >= 0)   ? in[g - R]    : 0.0f;
        tmp[l + BLOK] = (g + BLOK < n) ? in[g + BLOK] : 0.0f;
    }
    __syncthreads();                    // tunggu sampai seluruh tmp terisi
    if (g < n) {
        float s = 0.0f;
        for (int o = -R; o <= R; o++) s += tmp[l + o];
        out[g] = s;
    }
}

// Versi tanpa shared memory: setiap masukan dibaca 2R + 1 = 7 kali dari memori
// global oleh thread yang berbeda (cache L1/L2 membantu sebagian).
__global__ void stencil1d_global(const float *in, float *out, int n) {
    int g = blockIdx.x * blockDim.x + threadIdx.x;
    if (g < n) {
        float s = 0.0f;
        for (int o = -R; o <= R; o++) {
            int j = g + o;
            s += (j >= 0 && j < n) ? in[j] : 0.0f;
        }
        out[g] = s;
    }
}

// pembanding CPU dengan batas nol yang sama
static void stencil_cpu(const float *in, float *out, int n) {
    for (int g = 0; g < n; g++) {
        float s = 0.0f;
        for (int o = -R; o <= R; o++) {
            int j = g + o;
            if (j >= 0 && j < n) s += in[j];
        }
        out[g] = s;
    }
}

static float ukur(void (*k)(const float *, float *, int), const float *din, float *dout, int n) {
    int grid = (n + BLOK - 1) / BLOK;
    cudaEvent_t a, b;
    CEK(cudaEventCreate(&a)); CEK(cudaEventCreate(&b));
    k<<<grid, BLOK>>>(din, dout, n);              // pemanasan
    CEK(cudaGetLastError());
    CEK(cudaEventRecord(a));
    for (int r = 0; r < 10; r++) k<<<grid, BLOK>>>(din, dout, n);
    CEK(cudaEventRecord(b));
    CEK(cudaEventSynchronize(b));
    float ms; CEK(cudaEventElapsedTime(&ms, a, b));
    CEK(cudaEventDestroy(a)); CEK(cudaEventDestroy(b));
    return ms / 10;
}

static int periksa(const float *x, const float *ref, int n) {
    int salah = 0;
    for (int i = 0; i < n; i++)
        if (fabsf(x[i] - ref[i]) > 1e-3f * fmaxf(1.0f, fabsf(ref[i]))) salah++;
    return salah;
}

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : (1 << 24) + 5;
    size_t bytes = (size_t)n * sizeof(float);
    float *in = (float *)malloc(bytes), *out = (float *)malloc(bytes), *ref = (float *)malloc(bytes);
    for (int i = 0; i < n; i++) in[i] = (float)((i * 37) % 101) / 10.0f;
    stencil_cpu(in, ref, n);

    float *din, *dout;
    CEK(cudaMalloc(&din, bytes)); CEK(cudaMalloc(&dout, bytes));
    CEK(cudaMemcpy(din, in, bytes, cudaMemcpyHostToDevice));

    // blockDim.x HARUS sama dengan BLOK, karena kernel memuat halo kanan di tmp[l + BLOK]
    float ms_sh = ukur(stencil1d, din, dout, n);
    CEK(cudaMemcpy(out, dout, bytes, cudaMemcpyDeviceToHost));
    int salah_sh = periksa(out, ref, n);

    CEK(cudaMemset(dout, 0, bytes));
    float ms_gl = ukur(stencil1d_global, din, dout, n);
    CEK(cudaMemcpy(out, dout, bytes, cudaMemcpyDeviceToHost));
    int salah_gl = periksa(out, ref, n);

    printf("n = %d, R = %d, BLOK = %d\n", n, R, BLOK);
    printf("shared memory : %.3f ms, %s (%d salah)\n", ms_sh, salah_sh ? "GAGAL" : "benar", salah_sh);
    printf("memori global : %.3f ms, %s (%d salah)\n", ms_gl, salah_gl ? "GAGAL" : "benar", salah_gl);
    printf("contoh: out[0] = %.2f, out[n/2] = %.2f, out[n-1] = %.2f\n", ref[0], ref[n / 2], ref[n - 1]);

    CEK(cudaFree(din)); CEK(cudaFree(dout));
    free(in); free(out); free(ref);
    return (salah_sh || salah_gl) ? 1 : 0;
}
