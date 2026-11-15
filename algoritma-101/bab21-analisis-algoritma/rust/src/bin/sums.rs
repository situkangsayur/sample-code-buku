// Bab 21: loop pembagi (Algoritma 21.1) dan loop pelipatan dua.
// Banyak iterasi dicocokkan dengan rumus deret di buku.

fn divisor_counts(n: usize) -> (Vec<u32>, u64) {
    let mut d = vec![0u32; n + 1]; // indeks 0 tidak dipakai
    let mut steps = 0u64;
    for i in 1..=n {
        let mut j = i;
        while j <= n {
            d[j] += 1;
            steps += 1;
            j += i; // lompat ke kelipatan i berikutnya
        }
    }
    (d, steps)
}

fn doubling_loop(n: u64) -> u64 {
    let mut steps = 0;
    for i in 1..=n {
        let mut j = 1u64;
        while j <= i {
            j *= 2;
            steps += 1;
        }
    }
    steps
}

fn harmonic(n: usize) -> f64 {
    (1..=n).map(|k| 1.0 / k as f64).sum()
}

fn main() {
    let (d, s) = divisor_counts(6);
    assert_eq!(&d[1..], &[1, 2, 2, 3, 2, 4]);
    assert_eq!(s, 14);
    for n in [10usize, 100, 1000, 100_000] {
        let (_, s) = divisor_counts(n);
        let exact: u64 = (1..=n).map(|i| (n / i) as u64).sum();
        assert_eq!(s, exact);
        let nh = n as f64 * harmonic(n);
        assert!((s as f64) <= nh && (s as f64) > nh - n as f64);
        println!("divisor n={:>6}: langkah={:>8}  n*H_n={:>11.1}", n, s, nh);
    }
    for n in [1u64, 2, 8, 100, 1000] {
        let s = doubling_loop(n);
        let exact: u64 = (1..=n).map(|i| 64 - i.leading_zeros() as u64).sum();
        assert_eq!(s, exact);
        println!("doubling n={:>5}: langkah={:>6}", n, s);
    }
    println!("sums: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn divisor_six() {
        assert_eq!(divisor_counts(6).1, 14);
    }
    #[test]
    fn doubling_eight() {
        assert_eq!(doubling_loop(8), 21);
    }
}
