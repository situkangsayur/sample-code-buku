// RSA mainan dengan bilangan kecil (Algoritma 32.1, Kode 32.3).
// HANYA untuk belajar; RSA sungguhan memakai library yang sudah diaudit.

fn pangkat_mod(mut b: u64, mut e: u64, m: u64) -> u64 {
    let mut hasil: u64 = 1;
    b %= m;
    while e > 0 {
        if e & 1 == 1 {
            hasil = ((hasil as u128 * b as u128) % m as u128) as u64;
        }
        b = ((b as u128 * b as u128) % m as u128) as u64;
        e >>= 1;
    }
    hasil
}

fn invers_mod(e: i64, phi: i64) -> Option<i64> {
    let (mut r0, mut r1) = (phi, e);
    let (mut s0, mut s1) = (0i64, 1i64);
    while r1 != 0 {
        let q = r0 / r1;
        (r0, r1) = (r1, r0 - q * r1);
        (s0, s1) = (s1, s0 - q * s1);
    }
    if r0 != 1 {
        return None;
    }
    Some(s0.rem_euclid(phi))
}

fn main() {
    let (p, q, e) = (61u64, 53u64, 17u64);
    let n = p * q;
    let phi = (p - 1) * (q - 1);
    let d = invers_mod(e as i64, phi as i64).unwrap() as u64;
    println!("n = {}, e = {}, d = {}", n, e, d); // n = 3233, e = 17, d = 2753
    let c = pangkat_mod(65, e, n);
    println!("c = {}", c); // 2790
    println!("m = {}", pangkat_mod(c, d, n)); // 65
    for m in 0..n {
        assert_eq!(pangkat_mod(pangkat_mod(m, e, n), d, n), m);
    }
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contoh_buku() {
        assert_eq!(invers_mod(17, 3120), Some(2753));
        assert_eq!(pangkat_mod(65, 17, 3233), 2790);
        assert_eq!(invers_mod(6, 3120), None);
    }
}
