// Kode 7.3: Euclid di Rust dengan u64 (Algoritma 7.2).
fn euclid(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn main() {
    assert_eq!(euclid(252, 105), 21);
    assert_eq!(euclid(17, 0), 17);
    println!("euclid: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contoh_buku() {
        assert_eq!(euclid(1071, 462), 21);
        assert_eq!(euclid(105, 252), 21);
        assert_eq!(euclid(55, 34), 1);
    }
    #[test]
    fn sisa_negatif() {
        assert_eq!(-7i64 % 3, -1); // Rust mengikuti tanda bilangan yang dibagi
        assert_eq!((-7i64).rem_euclid(3), 2);
    }
}
