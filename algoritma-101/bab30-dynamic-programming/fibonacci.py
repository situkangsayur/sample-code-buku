"""Fibonacci dengan memoization (top-down) dan tabulation (bottom-up).

Bab 30 buku Algoritma 101, Algoritma 30.1 dan 26.2.
"""


def fib_memo(n, memo=None):
    """Top-down: rekursi biasa, tetapi setiap hasil disimpan di memo."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_tab(n):
    """Bottom-up: isi tabel F[0..n] dari kecil ke besar."""
    if n <= 1:
        return n
    f = [0] * (n + 1)
    f[1] = 1
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]
    return f[n]


def fib_naif(n, hitung):
    """Rekursi naif Bab 8; hitung[0] mencatat banyak pemanggilan."""
    hitung[0] += 1
    if n <= 1:
        return n
    return fib_naif(n - 1, hitung) + fib_naif(n - 2, hitung)


if __name__ == "__main__":
    for n in range(20):
        assert fib_memo(n) == fib_tab(n)
    assert fib_tab(10) == 55
    assert fib_tab(90) == 2880067194370816120
    h = [0]
    fib_naif(5, h)
    assert h[0] == 15  # 15 pemanggilan untuk fib(5)
    h = [0]
    fib_naif(30, h)
    assert h[0] == 2692537
    print("fib(10) =", fib_tab(10))
    print("pemanggilan naif fib(30) =", h[0])
    print("semua uji lolos")
