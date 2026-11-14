// Min-heap buatan sendiri dan BinaryHeap bawaan (Algoritma 19.2-19.3, Kode 19.5).
use std::cmp::Reverse;
use std::collections::BinaryHeap;

struct MinHeap {
    a: Vec<i32>,
}

impl MinHeap {
    fn push(&mut self, x: i32) {
        self.a.push(x);
        let mut i = self.a.len() - 1;
        while i > 0 && self.a[(i - 1) / 2] > self.a[i] {
            self.a.swap(i, (i - 1) / 2); // sift-up
            i = (i - 1) / 2;
        }
    }

    fn pop(&mut self) -> Option<i32> {
        let n = self.a.len();
        if n == 0 {
            return None;
        }
        self.a.swap(0, n - 1);
        let puncak = self.a.pop();
        let n = self.a.len();
        let mut i = 0;
        loop {
            // sift-down
            let mut kecil = i;
            for c in [2 * i + 1, 2 * i + 2] {
                if c < n && self.a[c] < self.a[kecil] {
                    kecil = c;
                }
            }
            if kecil == i {
                break;
            }
            self.a.swap(i, kecil);
            i = kecil;
        }
        puncak
    }
}

fn main() {
    let mut h = MinHeap { a: Vec::new() };
    for x in [15, 9, 12, 4, 7, 10, 2] {
        h.push(x);
    }
    assert_eq!(h.a, vec![2, 7, 4, 15, 9, 12, 10]);
    let mut keluar = Vec::new();
    while let Some(x) = h.pop() {
        keluar.push(x);
    }
    assert_eq!(keluar, vec![2, 4, 7, 9, 10, 12, 15]);

    // BinaryHeap bawaan adalah max-heap
    let mut maks = BinaryHeap::from(vec![15, 9, 12, 4]);
    assert_eq!(maks.pop(), Some(15));
    // Reverse membalik urutan sehingga menjadi min-heap
    let mut tugas = BinaryHeap::new();
    tugas.push(Reverse((3, "cetak laporan")));
    tugas.push(Reverse((1, "perbaiki server")));
    tugas.push(Reverse((2, "balas email")));
    assert_eq!(tugas.pop(), Some(Reverse((1, "perbaiki server"))));
    println!("heap: semua uji lolos");
}
