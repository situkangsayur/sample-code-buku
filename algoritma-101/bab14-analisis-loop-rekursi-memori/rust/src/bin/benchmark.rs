// Bab 14: mengukur waktu O(n) dan O(n^2) di Rust. Jalankan dengan
//   cargo run --release --bin benchmark
// Angka bergantung mesin. black_box mencegah compiler membuang perhitungan.
use std::hint::black_box;
use std::time::Instant;

fn sum_linear(a: &[i64]) -> i64 {
    let mut total = 0;
    for &v in a {
        total += v;
    }
    total
}

fn count_pairs(a: &[i64], x: i64) -> u64 {
    let n = a.len();
    let mut count = 0;
    for i in 0..n.saturating_sub(1) {
        for j in (i + 1)..n {
            if a[i] + a[j] == x {
                count += 1;
            }
        }
    }
    count
}

// pembangkit acak sederhana (LCG) agar tidak butuh crate tambahan
fn lcg(seed: &mut u64) -> u64 {
    *seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *seed >> 33
}

fn median_time<F: FnMut()>(mut f: F) -> f64 {
    let mut t = Vec::new();
    for _ in 0..5 {
        let start = Instant::now();
        f();
        t.push(start.elapsed().as_secs_f64());
    }
    t.sort_by(|a, b| a.partial_cmp(b).unwrap());
    t[2]
}

fn main() {
    let mut seed = 14u64;
    for n in [100_000usize, 1_000_000, 10_000_000] {
        let a: Vec<i64> = (0..n).map(|_| (lcg(&mut seed) % 1000 + 1) as i64).collect();
        let s = median_time(|| { black_box(sum_linear(black_box(&a))); });
        println!("O(n)   n={:>9}  {:.6} s", n, s);
    }
    for n in [1000usize, 2000, 4000, 8000, 16000] {
        let a: Vec<i64> = (0..n).map(|_| (lcg(&mut seed) % 1_000_000 + 1) as i64).collect();
        let s = median_time(|| { black_box(count_pairs(black_box(&a), 1_000_000)); });
        println!("O(n^2) n={:>9}  {:.6} s", n, s);
    }
    assert_eq!(count_pairs(&[3, 1, 4, 1, 5], 5), 2);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn small() {
        assert_eq!(sum_linear(&[1, 2, 3]), 6);
        assert_eq!(count_pairs(&[2, 2, 2], 4), 3);
    }
}
