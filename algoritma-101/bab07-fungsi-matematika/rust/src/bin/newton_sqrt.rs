// Algoritma 7.4 AkarNewton (f64) dan isqrt versi Newton, dicocokkan dengan u64::isqrt (Rust 1.84+).
fn akar_newton(a: f64, eps: f64, maks: u32) -> f64 {
    let mut x = a; // tebakan awal
    for _ in 0..maks {
        let baru = (x + a / x) / 2.0;
        if (baru - x).abs() < eps {
            return baru;
        }
        x = baru;
    }
    x
}

fn isqrt_newton(n: u64) -> u64 {
    if n < 2 {
        return n;
    }
    let mut x = n / 2 + 1; // tebakan awal >= akar n, tanpa overflow pada x + n / x
    loop {
        let y = (x + n / x) / 2;
        if y >= x {
            return x;
        }
        x = y;
    }
}

fn main() {
    assert!((akar_newton(2.0, 1e-12, 100) - 2f64.sqrt()).abs() < 1e-12);
    assert_eq!(isqrt_newton(10_000_000_000_000_000 - 1), 99_999_999);
    assert_eq!((10_000_000_000_000_000u64 - 1).isqrt(), 99_999_999);
    println!("newton_sqrt: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cocok_dengan_isqrt_bawaan() {
        for n in 0..20_000u64 {
            assert_eq!(isqrt_newton(n), n.isqrt());
        }
        for n in [u64::MAX, u64::MAX - 1, 1 << 63, 999_999_999_999_999_999] {
            assert_eq!(isqrt_newton(n), n.isqrt());
        }
    }
}
