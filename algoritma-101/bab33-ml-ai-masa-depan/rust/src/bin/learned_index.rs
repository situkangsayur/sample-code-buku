// Learned index: regresi linear + binary search di jendela error (Algoritma 33.2).

struct LearnedIndex {
    keys: Vec<u64>,
    a: f64,
    b: f64,
    err: i64,
}

impl LearnedIndex {
    fn new(keys: Vec<u64>) -> Self {
        let n = keys.len() as f64;
        let mx = keys.iter().map(|&k| k as f64).sum::<f64>() / n;
        let my = (n - 1.0) / 2.0;
        let (mut sxx, mut sxy) = (0.0, 0.0);
        for (i, &k) in keys.iter().enumerate() {
            sxx += (k as f64 - mx).powi(2);
            sxy += (k as f64 - mx) * (i as f64 - my);
        }
        let a = sxy / sxx;
        let b = my - a * mx;
        let mut li = LearnedIndex { keys, a, b, err: 0 };
        li.err = (0..li.keys.len())
            .map(|i| (li.tebak(li.keys[i]) - i as i64).abs())
            .max()
            .unwrap();
        li
    }
    fn tebak(&self, k: u64) -> i64 {
        (self.a * k as f64 + self.b).round() as i64
    }
    fn cari(&self, k: u64) -> Option<usize> {
        let p = self.tebak(k);
        let lo = (p - self.err).max(0) as usize;
        let hi = ((p + self.err).min(self.keys.len() as i64 - 1)).max(0) as usize;
        if lo > hi {
            return None;
        }
        self.keys[lo..=hi].binary_search(&k).ok().map(|j| lo + j)
    }
}

fn main() {
    // kunci hampir seragam: 0, 10, 20, ... ditambah gangguan kecil
    let keys: Vec<u64> = (0..100_000u64).map(|i| i * 10 + (i * 7919) % 7).collect();
    let li = LearnedIndex::new(keys.clone());
    println!("a = {:.4}, b = {:.2}, err maks = {}", li.a, li.b, li.err);
    for (i, &k) in keys.iter().enumerate().step_by(97) {
        assert_eq!(li.cari(k), Some(i));
    }
    assert_eq!(li.cari(3), keys.binary_search(&3).ok());
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn kunci_tidak_ada() {
        let li = LearnedIndex::new(vec![10, 20, 30, 40, 50]);
        assert_eq!(li.cari(30), Some(2));
        assert_eq!(li.cari(35), None);
        assert_eq!(li.cari(1000), None);
    }
}
