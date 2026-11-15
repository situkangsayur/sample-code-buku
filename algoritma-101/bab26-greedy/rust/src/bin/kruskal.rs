// Kruskal dengan union-find (Algoritma 26.6).

struct UnionFind {
    induk: Vec<usize>,
    ukuran: Vec<usize>,
}

impl UnionFind {
    fn new(n: usize) -> Self {
        UnionFind { induk: (0..n).collect(), ukuran: vec![1; n] }
    }
    fn find(&mut self, mut x: usize) -> usize {
        while self.induk[x] != x {
            self.induk[x] = self.induk[self.induk[x]]; // path halving
            x = self.induk[x];
        }
        x
    }
    fn union(&mut self, a: usize, b: usize) -> bool {
        let (mut ra, mut rb) = (self.find(a), self.find(b));
        if ra == rb {
            return false;
        }
        if self.ukuran[ra] < self.ukuran[rb] {
            std::mem::swap(&mut ra, &mut rb);
        }
        self.induk[rb] = ra;
        self.ukuran[ra] += self.ukuran[rb];
        true
    }
}

fn kruskal(n: usize, sisi: &mut Vec<(usize, usize, u32)>) -> (Vec<(usize, usize, u32)>, u32) {
    sisi.sort_by_key(|e| e.2); // stabil: urutan asli dipertahankan bila bobot sama
    let mut uf = UnionFind::new(n);
    let mut mst = Vec::new();
    let mut total = 0;
    for &(u, v, w) in sisi.iter() {
        if uf.union(u, v) {
            mst.push((u, v, w));
            total += w;
        }
    }
    (mst, total)
}

fn main() {
    let mut sisi = vec![(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8),
                        (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)];
    let (mst, total) = kruskal(6, &mut sisi);
    assert_eq!(total, 13);
    assert_eq!(mst, vec![(1, 2, 1), (0, 2, 2), (3, 4, 2), (4, 5, 3), (1, 3, 5)]);
    println!("kruskal: total {}, semua uji lolos", total);
}
