"""Las Vegas: mencari indeks berisi 'a' di array yang separuhnya 'a' (subbab 31.3).

Jawaban selalu benar; banyak percobaan acak, dengan rata-rata 2.
"""
import random


def cari_a(arr, rng=random):
    percobaan = 0
    while True:
        percobaan += 1
        i = rng.randrange(len(arr))
        if arr[i] == "a":
            return i, percobaan


if __name__ == "__main__":
    rng = random.Random(7)
    arr = ["a", "b"] * 500
    rng.shuffle(arr)
    total = 0
    for _ in range(10000):
        i, c = cari_a(arr, rng)
        assert arr[i] == "a"       # selalu benar
        total += c
    rata = total / 10000
    print(f"rata-rata percobaan: {rata:.3f}")   # dekat 2
    assert 1.9 < rata < 2.1
    print("semua uji lolos")
