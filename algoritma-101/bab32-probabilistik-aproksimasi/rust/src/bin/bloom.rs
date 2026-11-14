// Bloom filter dengan double hashing (Kode 32.3 versi Rust).
// Dua hash 64 bit diturunkan dari FNV-1a dan splitmix64, cukup untuk contoh.

fn fnv1a(data: &[u8]) -> u64 {
    let mut h: u64 = 0xcbf29ce484222325;
    for &b in data {
        h ^= b as u64;
        h = h.wrapping_mul(0x100000001b3);
    }
    h
}

fn splitmix(mut x: u64) -> u64 {
    x = x.wrapping_add(0x9e3779b97f4a7c15);
    x = (x ^ (x >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
    x = (x ^ (x >> 27)).wrapping_mul(0x94d049bb133111eb);
    x ^ (x >> 31)
}

struct BloomFilter {
    bit: Vec<bool>,
    k: u64,
}

impl BloomFilter {
    fn new(m: usize, k: u64) -> Self {
        BloomFilter { bit: vec![false; m], k }
    }
    fn posisi(&self, item: &str) -> Vec<usize> {
        let h1 = splitmix(fnv1a(item.as_bytes()));
        let h2 = splitmix(h1) | 1;
        let m = self.bit.len() as u64;
        (0..self.k).map(|i| (h1.wrapping_add(i.wrapping_mul(h2)) % m) as usize).collect()
    }
    fn tambah(&mut self, item: &str) {
        for p in self.posisi(item) {
            self.bit[p] = true;
        }
    }
    fn mungkin_ada(&self, item: &str) -> bool {
        self.posisi(item).iter().all(|&p| self.bit[p])
    }
}

fn main() {
    let (n, m, k) = (1000, 10000, 7);
    let mut bf = BloomFilter::new(m, k);
    for i in 0..n {
        bf.tambah(&format!("user{}", i));
    }
    let uji = 100_000;
    let fp = (0..uji).filter(|i| bf.mungkin_ada(&format!("tamu{}", i))).count();
    let teori = (1.0 - (-(k as f64) * n as f64 / m as f64).exp()).powi(k as i32);
    println!("false positive teramati {:.4}, rumus {:.4}", fp as f64 / uji as f64, teori);
    assert!((fp as f64 / uji as f64 - teori).abs() < 0.004);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn tanpa_false_negative() {
        let mut bf = BloomFilter::new(2000, 5);
        for i in 0..200 {
            bf.tambah(&i.to_string());
        }
        assert!((0..200).all(|i| bf.mungkin_ada(&i.to_string())));
    }
}
