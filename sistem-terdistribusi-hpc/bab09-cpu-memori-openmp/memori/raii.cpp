// Kode 9.3: RAII dan smart pointer (C++17).
#include <cstdio>
#include <memory>
#include <vector>

struct Config {
    int ukuran = 1024;
    ~Config() { std::puts("Config dibebaskan"); }
};

void proses() {
    auto buf = std::make_unique<double[]>(1000000);   // satu pemilik
    std::vector<int> v(1000);                          // vector juga RAII
    auto bersama = std::make_shared<Config>();
    auto salinan = bersama;                            // reference count = 2
    std::printf("use_count = %ld, buf[0] = %.1f, v.size = %zu\n",
                bersama.use_count(), buf[0], v.size());
}   // semua dibebaskan di sini, tanpa free/delete

int main() {
    proses();
    std::puts("selesai");
    return 0;
}
