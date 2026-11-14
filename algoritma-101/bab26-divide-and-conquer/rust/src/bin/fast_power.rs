// Pangkat cepat modulo m.

fn fast_power(a: u64, n: u64, m: u64) -> u64 {
    if n == 0 {
        return 1 % m;
    }
    let half = fast_power(a, n / 2, m) as u128;
    let mut hasil = half * half % m as u128; // u128 mencegah overflow
    if n % 2 == 1 {
        hasil = hasil * (a % m) as u128 % m as u128;
    }
    hasil as u64
}

fn main() {
    let m = 1_000_000_007;
    println!("{}", fast_power(3, 13, m)); // 1594323
    assert_eq!(fast_power(3, 13, m), 1594323);
    println!("{}", fast_power(2, 1_000_000_000_000, m));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cocok_dengan_pow() {
        for a in 0..10u64 {
            for n in 0..18u32 {
                assert_eq!(fast_power(a, n as u64, u64::MAX), a.pow(n));
            }
        }
    }
}
