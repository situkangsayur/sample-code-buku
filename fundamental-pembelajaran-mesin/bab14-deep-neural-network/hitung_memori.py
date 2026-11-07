"""Taksiran kasar memori pelatihan: parameter + gradien + status Adam (fp32),
tanpa aktivasi. Kode 11.4 pada buku."""


def memori_latih_byte(n_param, byte_param=4, byte_grad=4, byte_optim=8):
    # Adam menyimpan dua momen per parameter: 2 x 4 byte
    return n_param * (byte_param + byte_grad + byte_optim)


def rapi(n_byte):
    for satuan, b in (("GB", 1e9), ("MB", 1e6), ("KB", 1e3)):
        if n_byte >= b:
            return f"{n_byte / b:8.1f} {satuan}"
    return f"{n_byte:8.0f} B"


for nama, n in [("MLP MNIST (Bab 9)", 235_146),
                ("ResNet-50", 25_600_000),
                ("model bahasa 7 miliar parameter", 7_000_000_000)]:
    print(f"{nama:34s} parameter={n:>15,d}  memori latih ~ {rapi(memori_latih_byte(n))}"
          f"  (inferensi fp16 ~ {rapi(n * 2)})")
