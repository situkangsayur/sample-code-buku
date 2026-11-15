// Bab 39: HyperLogLog sederhana (p bit teratas memilih register).
use bab37_streaming_cache::h64;

struct Hll {
    p: u32,
    reg: Vec<u8>,
}

impl Hll {
    fn new(p: u32) -> Self {
        Hll { p, reg: vec![0; 1 << p] }
    }
    fn add(&mut self, item: &str) {
        let h = h64(item);
        let idx = (h >> (64 - self.p)) as usize;
        let rest = h << self.p;
        // posisi bit 1 pertama pada sisa bit, dibatasi 64 - p + 1
        let rank = (rest.leading_zeros() + 1).min(64 - self.p + 1) as u8;
        if rank > self.reg[idx] {
            self.reg[idx] = rank;
        }
    }
    fn count(&self) -> f64 {
        let m = self.reg.len() as f64;
        let alpha = 0.7213 / (1.0 + 1.079 / m);
        let z: f64 = self.reg.iter().map(|&r| 2f64.powi(-(r as i32))).sum();
        let mut e = alpha * m * m / z;
        let zeros = self.reg.iter().filter(|&&r| r == 0).count() as f64;
        if e <= 2.5 * m && zeros > 0.0 {
            e = m * (m / zeros).ln();
        }
        e
    }
}

fn main() {
    for &n in &[1_000usize, 10_000, 100_000] {
        let mut h = Hll::new(10);
        for i in 0..n {
            h.add(&format!("user-{}", i));
        }
        let est = h.count();
        let err = (est - n as f64).abs() / n as f64 * 100.0;
        println!("n = {:>7}: taksiran = {:.0}, galat = {:.2}%", n, est, err);
        assert!(err < 13.0);
    }
    println!("semua uji hyperloglog lolos");
}
