"""Bab 15: array dinamis di atas blok berkapasitas tetap.

Blok tetap ditiru dengan [None] * capacity; kita tidak memakai append bawaan list
agar setiap penyalinan terlihat dan dapat dihitung.
"""


class DynamicArray:
    def __init__(self, capacity=1):
        self._cap = capacity
        self._n = 0
        self._data = [None] * capacity
        self.copies = 0               # banyak elemen yang pernah disalin

    def __len__(self):
        return self._n

    def get(self, i):
        if not 0 <= i < self._n:
            raise IndexError("indeks di luar batas")
        return self._data[i]

    def set(self, i, value):
        if not 0 <= i < self._n:
            raise IndexError("indeks di luar batas")
        self._data[i] = value

    def _resize(self, new_cap):
        new_data = [None] * new_cap
        for k in range(self._n):
            new_data[k] = self._data[k]
            self.copies += 1
        self._data = new_data
        self._cap = new_cap

    def append(self, value):
        if self._n == self._cap:
            self._resize(2 * self._cap)
        self._data[self._n] = value
        self._n += 1

    def insert(self, i, value):
        """Sisipkan di indeks i (0 <= i <= n); elemen i..n-1 digeser ke kanan."""
        if not 0 <= i <= self._n:
            raise IndexError("indeks di luar batas")
        if self._n == self._cap:
            self._resize(2 * self._cap)
        for k in range(self._n, i, -1):
            self._data[k] = self._data[k - 1]
        self._data[i] = value
        self._n += 1

    def remove_at(self, i):
        """Hapus elemen di indeks i; elemen sesudahnya digeser ke kiri."""
        if not 0 <= i < self._n:
            raise IndexError("indeks di luar batas")
        value = self._data[i]
        for k in range(i, self._n - 1):
            self._data[k] = self._data[k + 1]
        self._data[self._n - 1] = None
        self._n -= 1
        return value

    def to_list(self):
        return [self._data[k] for k in range(self._n)]

    def capacity(self):
        return self._cap


def main():
    a = DynamicArray()
    caps = []
    for v in [10, 20, 30, 40, 50]:
        a.append(v)
        caps.append(a.capacity())
    print("kapasitas setelah tiap append:", caps)   # [1, 2, 4, 4, 8]
    assert caps == [1, 2, 4, 4, 8]
    assert a.copies == 1 + 2 + 4
    a.insert(1, 15)
    assert a.to_list() == [10, 15, 20, 30, 40, 50]
    assert a.remove_at(0) == 10
    assert a.to_list() == [15, 20, 30, 40, 50]
    a.set(2, 99)
    assert a.get(2) == 99 and len(a) == 5
    b = DynamicArray()
    for v in range(1000):
        b.append(v)
    assert b.copies < 2 * 1000
    try:
        a.get(5)
        assert False
    except IndexError:
        pass
    print("semua uji lolos")


if __name__ == "__main__":
    main()
