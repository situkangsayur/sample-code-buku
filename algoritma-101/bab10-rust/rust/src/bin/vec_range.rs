// Bab 10: range, Vec, dan slice.
// Jalankan: cargo run --bin vec_range ; uji: cargo test --bin vec_range

/// Rata-rata isi slice; None bila kosong.
fn rata_rata(a: &[f64]) -> Option<f64> {
    if a.is_empty() {
        return None;
    }
    let mut total = 0.0;
    for x in a {
        // for-each: x bertipe &f64
        total += *x;
    }
    Some(total / a.len() as f64)
}

/// Mengisi Vec dengan kuadrat 1..=n.
fn kuadrat(n: usize) -> Vec<usize> {
    let mut v = Vec::with_capacity(n);
    for i in 1..=n {
        v.push(i * i);
    }
    v
}

fn main() {
    let nilai = vec![70.0, 85.0, 90.0, 65.0];
    println!("rata-rata = {:?}", rata_rata(&nilai)); // Some(77.5)
    println!("potongan [1..3] = {:?}", &nilai[1..3]); // [85.0, 90.0]
    println!("get(10) = {:?}", nilai.get(10)); // None, tanpa panic
    println!("kuadrat(5) = {:?}", kuadrat(5));
    for i in (1..=3).rev() {
        print!("{} ", i); // 3 2 1
    }
    println!();
    for (i, x) in nilai.iter().enumerate() {
        println!("indeks {} -> {}", i, x);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uji_vec() {
        let nilai = vec![70.0, 85.0, 90.0, 65.0];
        assert_eq!(rata_rata(&nilai), Some(77.5));
        assert_eq!(rata_rata(&[]), None);
        assert_eq!(&nilai[1..3], &[85.0, 90.0]);
        assert_eq!(nilai.get(10), None);
        assert_eq!(kuadrat(5), vec![1, 4, 9, 16, 25]);
        assert_eq!((0..5).count(), 5); // 0..5 tidak memuat 5
        assert_eq!((0..=5).count(), 6);
        let mut v = vec![1, 2, 3];
        v.push(4);
        v.insert(0, 0);
        assert_eq!(v, vec![0, 1, 2, 3, 4]);
        assert_eq!(v.pop(), Some(4));
    }

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn akses_di_luar_batas() {
        let v = vec![1, 2, 3];
        let i = std::hint::black_box(3);
        let _ = v[i];
    }
}
