// Bab 35: Bloom filter dengan double hashing g_i(x) = h1 + i*h2 mod m.
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

struct Bloom {
    bits: Vec<bool>,
    k: u64,
}

impl Bloom {
    fn new(m: usize, k: u64) -> Self {
        Bloom { bits: vec![false; m], k }
    }
    fn hash<T: Hash>(x: &T, benih: u64) -> u64 {
        let mut h = DefaultHasher::new(); // kunci tetap, hasil deterministik
        benih.hash(&mut h);
        x.hash(&mut h);
        h.finish()
    }
    fn posisi<T: Hash>(&self, x: &T) -> Vec<usize> {
        let (h1, h2) = (Self::hash(x, 1), Self::hash(x, 2) | 1);
        let m = self.bits.len() as u64;
        (0..self.k).map(|i| (h1.wrapping_add(i.wrapping_mul(h2)) % m) as usize).collect()
    }
    fn add<T: Hash>(&mut self, x: &T) {
        for p in self.posisi(x) {
            self.bits[p] = true;
        }
    }
    fn mungkin_ada<T: Hash>(&self, x: &T) -> bool {
        self.posisi(x).iter().all(|&p| self.bits[p])
    }
}

fn main() {
    let mut b = Bloom::new(9586, 7); // n = 1000, p = 0,01
    for i in 0..1000u32 {
        b.add(&i);
    }
    assert!((0..1000u32).all(|i| b.mungkin_ada(&i))); // tanpa false negative
    let fp = (100_000..200_000u32).filter(|i| b.mungkin_ada(i)).count();
    let laju = fp as f64 / 100_000.0;
    println!("false positive: {:.4}", laju);
    assert!(laju < 0.02);
}
