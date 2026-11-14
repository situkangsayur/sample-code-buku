// Bab 11: linear search di Rust.
// Option<usize>: Some(i) bila ketemu, None bila tidak (pengganti 0 di pseudocode).

fn linear_search(a: &[i32], x: i32) -> Option<usize> {
    for i in 0..a.len() {
        if a[i] == x {
            return Some(i);
        }
    }
    None
}

fn main() {
    let nilai = [42, 17, 8, 99, 23, 8];
    println!("cari 99 -> {:?}", linear_search(&nilai, 99)); // Some(3)
    println!("cari 5  -> {:?}", linear_search(&nilai, 5)); // None
    match linear_search(&nilai, 8) {
        Some(i) => println!("8 pertama kali di indeks {}", i),
        None => println!("8 tidak ada"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uji_linear() {
        let nilai = [42, 17, 8, 99, 23, 8];
        assert_eq!(linear_search(&nilai, 99), Some(3));
        assert_eq!(linear_search(&nilai, 8), Some(2));
        assert_eq!(linear_search(&nilai, 42), Some(0));
        assert_eq!(linear_search(&nilai, 5), None);
        assert_eq!(linear_search(&[], 5), None);
        for x in [42, 17, 8, 99, 23, 5] {
            assert_eq!(linear_search(&nilai, x), nilai.iter().position(|&v| v == x));
        }
    }
}
