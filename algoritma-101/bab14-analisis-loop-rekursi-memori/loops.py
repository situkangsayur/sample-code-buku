"""Bab 14: menghitung banyak iterasi berbagai bentuk loop dan mencocokkannya dengan rumus."""


def sequential(n):
    steps = 0
    for _ in range(n):
        steps += 1
    for _ in range(n):
        steps += 1
    return steps                      # 2n -> O(n)


def nested(n):
    steps = 0
    for _ in range(n):
        for _ in range(n):
            steps += 1
    return steps                      # n^2 -> O(n^2)


def triangular(n):
    steps = 0
    for i in range(1, n + 1):         # i = 1..n seperti pseudocode
        for _ in range(1, i + 1):     # j = 1..i
            steps += 1
    return steps                      # n(n+1)/2 -> O(n^2)


def halving(n):
    steps = 0
    i = n
    while i > 1:
        i //= 2
        steps += 1
    return steps                      # floor(log2 n) -> O(log n)


def nested_log(n):
    steps = 0
    for _ in range(n):
        j = 1
        while j < n:
            j *= 2
            steps += 1
    return steps                      # n * ceil(log2 n) -> O(n log n)


def main():
    for n in [1, 2, 7, 8, 100, 1000]:
        assert sequential(n) == 2 * n
        assert nested(n) == n * n
        assert triangular(n) == n * (n + 1) // 2
        assert halving(n) == (n.bit_length() - 1)
        assert nested_log(n) == n * (n - 1).bit_length()
    print("n=16:", sequential(16), nested(16), triangular(16), halving(16), nested_log(16))
    # 32 256 136 4 64
    print("semua uji lolos")


if __name__ == "__main__":
    main()
