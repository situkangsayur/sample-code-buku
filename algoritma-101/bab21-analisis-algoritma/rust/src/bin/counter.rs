// Bab 21: counter biner (Algoritma 21.3) dan analisis amortized.
// bits[0] adalah bit paling kanan. Biaya increment = banyak bit yang dibalik.

fn increment(bits: &mut [u8]) -> u32 {
    let mut i = 0;
    let mut flips = 0;
    while i < bits.len() && bits[i] == 1 {
        bits[i] = 0; // 1 -> 0
        flips += 1;
        i += 1;
    }
    if i < bits.len() {
        bits[i] = 1; // 0 -> 1
        flips += 1;
    }
    flips
}

// potential Phi = banyak bit 1
fn ones(b: &[u8]) -> i64 { b.iter().map(|&x| x as i64).sum() }

fn main() {
    let mut bits = [0u8; 5];
    let mut total = 0u32;
    for step in 1..=16u32 {
        let before = ones(&bits);
        let c = increment(&mut bits);
        total += c;
        let amortized = c as i64 + ones(&bits) - before;
        assert_eq!(amortized, 2); // biaya amortized
        assert!(total < 2 * step);
        let s: String = bits.iter().rev().map(|b| char::from(b'0' + b)).collect();
        println!("{:>2} {} biaya={} total={}", step, s, c, total);
    }
    let mut big = [0u8; 20];
    let n = 100_000u64;
    let total: u64 = (0..n).map(|_| increment(&mut big) as u64).sum();
    assert!(total < 2 * n);
    println!("n={}: total balik bit = {}", n, total);
    println!("counter: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn eight_increments() {
        let mut b = [0u8; 4];
        let t: u32 = (0..8).map(|_| increment(&mut b)).sum();
        assert_eq!(t, 15);
        assert_eq!(b, [0, 0, 0, 1]);
    }
}
