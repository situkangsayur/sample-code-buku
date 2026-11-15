//! Fungsi hash bersama untuk Bab 39 (sama persis dengan versi Python).

/// Hash FNV-1a 64 bit.
pub fn fnv1a64(data: &[u8]) -> u64 {
    let mut h: u64 = 0xcbf29ce484222325;
    for &b in data {
        h ^= b as u64;
        h = h.wrapping_mul(0x100000001b3);
    }
    h
}

/// Finalizer splitmix64 untuk meratakan bit.
pub fn mix64(mut x: u64) -> u64 {
    x ^= x >> 30;
    x = x.wrapping_mul(0xbf58476d1ce4e5b9);
    x ^= x >> 27;
    x = x.wrapping_mul(0x94d049bb133111eb);
    x ^= x >> 31;
    x
}

pub fn h64(s: &str) -> u64 {
    mix64(fnv1a64(s.as_bytes()))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn fnv_test_vectors() {
        assert_eq!(fnv1a64(b""), 0xcbf29ce484222325);
        assert_eq!(fnv1a64(b"a"), 0xaf63dc4c8601ec8c);
    }
}
