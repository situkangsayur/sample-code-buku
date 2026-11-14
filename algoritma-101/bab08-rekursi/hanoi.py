"""Algoritma 8.2 Hanoi: memindahkan n cakram dari tiang asal ke tujuan."""


def hanoi(n: int, asal: str, tujuan: str, bantu: str, langkah: list) -> None:
    if n > 0:
        hanoi(n - 1, asal, bantu, tujuan, langkah)
        langkah.append((n, asal, tujuan))
        hanoi(n - 1, bantu, tujuan, asal, langkah)


if __name__ == "__main__":
    langkah = []
    hanoi(3, "A", "C", "B", langkah)
    for i, (n, a, t) in enumerate(langkah, 1):
        print(f"{i}. cakram {n}: {a} -> {t}")
    assert langkah == [(1, "A", "C"), (2, "A", "B"), (1, "C", "B"), (3, "A", "C"),
                       (1, "B", "A"), (2, "B", "C"), (1, "A", "C")]
    for n in range(12):
        L = []
        hanoi(n, "A", "C", "B", L)
        assert len(L) == 2**n - 1
    print("hanoi.py: semua uji lolos")
