// Algoritma 7.3 PangkatCepat di Rust: versi u64 dengan checked_mul dan versi modulo dengan u128.
fn pangkat_cepat(mut a: u64, mut n: u32) -> Option<u64> {
    let mut hasil: u64 = 1;
    while n > 0 {
        if n % 2 == 1 {
            hasil = hasil.checked_mul(a)?;
        }
        n /= 2;
        if n > 0 {
            a = a.checked_mul(a)?; // kuadrat dilewati bila tidak dipakai lagi
        }
    }
    Some(hasil)
}

fn pangkat_mod(a: u64, mut n: u64, m: u64) -> u64 {
    let m128 = m as u128;
    let mut hasil: u128 = 1;
    let mut a = (a % m) as u128;
    while n > 0 {
        if n % 2 == 1 {
            hasil = hasil * a % m128; // u128 agar perkalian tidak overflow
        }
        a = a * a % m128;
        n /= 2;
    }
    hasil as u64
}

fn main() {
    assert_eq!(pangkat_cepat(3, 13), Some(1_594_323));
    assert_eq!(pangkat_cepat(3, 40), Some(12_157_665_459_056_928_801));
    assert_eq!(pangkat_cepat(3, 41), None);
    assert_eq!(pangkat_mod(3, 13, 1_000_000_007), 1_594_323);
    println!("pangkat_cepat: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sama_dengan_pow() {
        for n in 0..=40u32 {
            assert_eq!(pangkat_cepat(3, n), Some(3u64.pow(n)));
        }
    }
    #[test]
    fn modulo_besar() {
        // 7^(10^18) mod (10^9+7), dicocokkan dengan pow(7, 10**18, 10**9 + 7) di Python
        assert_eq!(pangkat_mod(7, 1_000_000_000_000_000_000, 1_000_000_007), EXPECTED);
    }
    const EXPECTED: u64 = 259616729; // pow(7, 10**18, 10**9 + 7) di Python
}
