// Kode 4.7: bagging dengan decision stump dan suara terbanyak, dari nol.
// Pembangkit acak sederhana (LCG), cukup untuk ilustrasi
struct Lcg(u64);
impl Lcg {
    fn next(&mut self, n: usize) -> usize {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((self.0 >> 33) as usize) % n
    }
}

// Stump: ambang dan polaritas dengan kesalahan terkecil
fn latih_stump(x: &[f64], y: &[i32]) -> (f64, i32) {
    let mut terbaik = (usize::MAX, 0.0, 1);
    for &th in x {
        for pol in [1, -1] {
            let salah = x.iter().zip(y)
                .filter(|(xi, yi)| (if **xi <= th { pol } else { -pol }) != **yi)
                .count();
            if salah < terbaik.0 { terbaik = (salah, th, pol); }
        }
    }
    (terbaik.1, terbaik.2)
}

fn main() {
    let x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0];
    let y = [1, 1, 1, 1, -1, 1, -1, -1];      // baris ke-6 ber-noise
    let (n, b) = (x.len(), 25);
    let mut rng = Lcg(42);
    let mut hutan = Vec::new();
    for _ in 0..b {
        // bootstrap: n pengambilan dengan pengembalian
        let idx: Vec<usize> = (0..n).map(|_| rng.next(n)).collect();
        let xb: Vec<f64> = idx.iter().map(|&i| x[i]).collect();
        let yb: Vec<i32> = idx.iter().map(|&i| y[i]).collect();
        hutan.push(latih_stump(&xb, &yb));
    }
    for &q in &[2.5, 4.5, 5.5, 7.5] {
        let suara: i32 = hutan.iter()
            .map(|&(th, pol)| if q <= th { pol } else { -pol }).sum();
        let kelas = if suara >= 0 { 1 } else { -1 };
        println!("x={q}: total suara={suara:+}, kelas={kelas:+}");
    }
}
