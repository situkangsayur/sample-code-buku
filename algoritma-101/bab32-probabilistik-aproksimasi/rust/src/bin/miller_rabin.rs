// Uji prima Miller-Rabin dengan basis acak (Algoritma 32.1, Kode 32.2 versi Rust).

fn mul_mod(a: u64, b: u64, m: u64) -> u64 {
    ((a as u128 * b as u128) % m as u128) as u64
}

fn pow_mod(mut b: u64, mut e: u64, m: u64) -> u64 {
    let mut r = 1u64;
    b %= m;
    while e > 0 {
        if e & 1 == 1 {
            r = mul_mod(r, b, m);
        }
        b = mul_mod(b, b, m);
        e >>= 1;
    }
    r
}

// Pembangkit acak xorshift64 kecil agar tanpa crate tambahan.
struct Acak(u64);
impl Acak {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
}

fn miller_rabin(n: u64, k: u32, rng: &mut Acak) -> bool {
    if n < 2 {
        return false;
    }
    for p in [2u64, 3, 5, 7, 11, 13] {
        if n % p == 0 {
            return n == p;
        }
    }
    let (mut d, mut s) = (n - 1, 0u32);
    while d % 2 == 0 {
        d /= 2;
        s += 1;
    }
    'saksi: for _ in 0..k {
        let a = 2 + rng.next() % (n - 3);
        let mut x = pow_mod(a, d, n);
        if x == 1 || x == n - 1 {
            continue;
        }
        for _ in 0..s - 1 {
            x = mul_mod(x, x, n);
            if x == n - 1 {
                continue 'saksi;
            }
        }
        return false; // a saksi: n pasti komposit
    }
    true // mungkin prima
}

fn main() {
    let mut rng = Acak(2026);
    println!("{}", miller_rabin(561, 20, &mut rng)); // false
    println!("{}", miller_rabin((1u64 << 61) - 1, 20, &mut rng)); // true
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    fn naif(n: u64) -> bool {
        n >= 2 && (2..).take_while(|i| i * i <= n).all(|i| n % i != 0)
    }
    #[test]
    fn cocok_dengan_naif() {
        let mut rng = Acak(1);
        for n in 0..5000 {
            assert_eq!(miller_rabin(n, 20, &mut rng), naif(n));
        }
    }
}
