// Hash polinomial untuk hash table dan efek avalanche (Kode 32.4 versi Rust).
// Pustaka standar Rust tidak menyediakan SHA-256; untuk itu pakai crate sha2.

fn hash_tabel(s: &str) -> u32 {
    let mut h: u32 = 0;
    for b in s.bytes() {
        h = h.wrapping_mul(31).wrapping_add(b as u32); // mod 2^32
    }
    h
}

fn main() {
    let (a, b) = ("transfer 100", "transfer 101");
    let (ha, hb) = (hash_tabel(a), hash_tabel(b));
    println!("{:#x} {:#x}", ha, hb);
    println!("bit berubah: {} dari 32", (ha ^ hb).count_ones()); // 1
    assert_eq!(hash_tabel("Aa"), hash_tabel("BB")); // tabrakan mudah
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn tabrakan() {
        assert_eq!(hash_tabel("Aa"), 2112);
        assert_eq!(hash_tabel("BB"), 2112);
    }
}
