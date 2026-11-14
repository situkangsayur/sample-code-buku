// Kode 8.3: Fibonacci iteratif di Rust, ditambah versi rekursif dengan penghitung
// dan versi checked_add yang menangani batas u64.
fn fib_iter(n: u32) -> u64 {
    let (mut a, mut b): (u64, u64) = (0, 1);
    for _ in 0..n {
        let c = a + b; // panic bila overflow (mode debug)
        a = b;
        b = c;
    }
    a
}

fn fib_iter_aman(n: u32) -> Option<u64> {
    let (mut a, mut b): (u64, u64) = (0, 1);
    for _ in 0..n {
        let c = a.checked_add(b)?;
        a = b;
        b = c;
    }
    Some(a)
}

fn fib_rek(n: u32, panggilan: &mut u64) -> u64 {
    *panggilan += 1;
    if n <= 1 {
        return n as u64;
    }
    fib_rek(n - 1, panggilan) + fib_rek(n - 2, panggilan)
}

fn main() {
    assert_eq!(fib_iter(20), 6765);
    assert_eq!(fib_iter(90), 2_880_067_194_370_816_120);
    let mut c = 0;
    assert_eq!(fib_rek(20, &mut c), 6765);
    assert_eq!(c, 21_891);
    assert_eq!(fib_iter_aman(93), None); // b harus menyimpan F(94)
    println!("fibonacci: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn batas_u64() {
        // F(93) masih muat, tetapi loop menghitung F(94) di b sehingga checked_add gagal
        assert_eq!(fib_iter_aman(92), Some(7_540_113_804_746_346_429));
        assert_eq!(fib_iter_aman(93), None);
        assert_eq!(fib_iter(92), 7_540_113_804_746_346_429);
    }
    #[test]
    fn banyak_panggilan() {
        for n in 0..25u32 {
            let mut c = 0;
            fib_rek(n, &mut c);
            assert_eq!(c, 2 * fib_iter(n + 1) - 1);
        }
    }
}
