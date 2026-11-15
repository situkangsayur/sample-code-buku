// Uji stres: solusi cepat vs brute force (Kode 34.2 versi Rust).

fn brute_force(a: &[i64]) -> i64 {
    let mut terbaik = i64::MIN;
    for i in 0..a.len() {
        let mut s = 0;
        for x in &a[i..] {
            s += x;
            terbaik = terbaik.max(s);
        }
    }
    terbaik
}

fn solusi_cepat_salah(a: &[i64]) -> i64 {
    let (mut terbaik, mut kini) = (0i64, 0i64); // BUG: mulai dari 0
    for &x in a {
        kini = (kini + x).max(0);
        terbaik = terbaik.max(kini);
    }
    terbaik
}

fn kadane(a: &[i64]) -> i64 {
    let (mut terbaik, mut kini) = (a[0], a[0]);
    for &x in &a[1..] {
        kini = x.max(kini + x);
        terbaik = terbaik.max(kini);
    }
    terbaik
}

struct Acak(u64);
impl Acak {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
}

fn uji_stres(f: fn(&[i64]) -> i64, percobaan: u32) -> Option<Vec<i64>> {
    let mut rng = Acak(88172645463325252);
    for _ in 0..percobaan {
        let n = 1 + (rng.next() % 6) as usize;
        let a: Vec<i64> = (0..n).map(|_| (rng.next() % 11) as i64 - 5).collect();
        if f(&a) != brute_force(&a) {
            return Some(a);
        }
    }
    None
}

fn main() {
    let c = uji_stres(solusi_cepat_salah, 1000).expect("harus ada contoh penyangkal");
    println!("contoh penyangkal {:?}: cepat {} brute {}", c, solusi_cepat_salah(&c), brute_force(&c));
    assert!(uji_stres(kadane, 1000).is_none());
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn semua_negatif() {
        assert_eq!(kadane(&[-3, -1, -2]), -1);
        assert_eq!(solusi_cepat_salah(&[-3, -1, -2]), 0);
    }
}
