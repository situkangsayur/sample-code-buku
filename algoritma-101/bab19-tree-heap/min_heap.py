"""Min-heap berbasis array (Algoritma 19.2 dan 19.3, Kode 19.3) dan heapq (Kode 19.4).

Pseudocode di buku memakai indeks 1: anak i adalah 2i dan 2i+1.
Python memakai indeks 0: anak i adalah 2i+1 dan 2i+2, parent (i-1)//2.
"""
import heapq


class MinHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and a[(i - 1) // 2] > a[i]:      # sift-up
            p = (i - 1) // 2
            a[i], a[p] = a[p], a[i]
            i = p

    def pop(self):
        a = self.a
        akhir = a.pop()
        if not a:
            return akhir
        puncak = a[0]
        a[0] = akhir
        i = 0
        n = len(a)
        while True:                                   # sift-down
            kecil = i
            for c in (2 * i + 1, 2 * i + 2):
                if c < n and a[c] < a[kecil]:
                    kecil = c
            if kecil == i:
                break
            a[i], a[kecil] = a[kecil], a[i]
            i = kecil
        return puncak

    def __len__(self):
        return len(self.a)


if __name__ == "__main__":
    h = MinHeap()
    jejak = []
    for x in [15, 9, 12, 4, 7, 10, 2]:
        h.push(x)
        jejak.append(list(h.a))
    # isi array setelah tiap push (Tabel 19.3)
    assert jejak[-1] == [2, 7, 4, 15, 9, 12, 10], jejak[-1]
    keluar = [h.pop() for _ in range(len(h))]
    assert keluar == [2, 4, 7, 9, 10, 12, 15]

    # heapq bawaan: fungsi atas list biasa, juga min-heap
    tugas = []
    heapq.heappush(tugas, (3, "cetak laporan"))
    heapq.heappush(tugas, (1, "perbaiki server"))
    heapq.heappush(tugas, (2, "balas email"))
    assert heapq.heappop(tugas) == (1, "perbaiki server")
    assert [heapq.heappop(tugas)[1] for _ in range(2)] == ["balas email", "cetak laporan"]
    # heapify: mengubah list menjadi heap dalam O(n)
    data = [15, 9, 12, 4, 7, 10, 2]
    heapq.heapify(data)
    assert data[0] == 2
    assert heapq.nsmallest(3, [15, 9, 12, 4, 7, 10, 2]) == [2, 4, 7]
    print("min_heap.py: semua uji lolos")
    for j in jejak:
        print(j)
