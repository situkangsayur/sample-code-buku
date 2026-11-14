// Bab 11: algoritma mudah di Rust.
// Jalankan: cargo run --bin algoritma_mudah ; uji: cargo test --bin algoritma_mudah

/// Nilai terbesar dan indeks pertamanya. None bila slice kosong.
fn maks_dan_posisi(a: &[i32]) -> Option<(i32, usize)> {
    if a.is_empty() {
        return None;
    }
    let (mut maks, mut pos) = (a[0], 0);
    for i in 1..a.len() {
        if a[i] > maks {
            maks = a[i];
            pos = i;
        }
    }
    Some((maks, pos))
}

/// Jumlah elemen. i64 agar tidak mudah overflow.
fn jumlah(a: &[i32]) -> i64 {
    let mut s: i64 = 0;
    for &x in a {
        s += x as i64;
    }
    s
}

/// Tukar a[i] dan a[j] dengan variabel bantu (padanan pseudocode).
fn tukar(a: &mut [i32], i: usize, j: usize) {
    let temp = a[i];
    a[i] = a[j];
    a[j] = temp;
}

/// Uji prima dengan pembagi d sampai d * d <= n.
fn is_prima(n: u64) -> bool {
    if n < 2 {
        return false;
    }
    let mut d = 2;
    while d * d <= n {
        if n % d == 0 {
            return false;
        }
        d += 1;
    }
    true
}

/// Konversi ke string biner dengan pembagian berulang.
fn ke_biner(mut n: u64) -> String {
    if n == 0 {
        return String::from("0");
    }
    let mut digit = Vec::new();
    while n > 0 {
        digit.push(if n % 2 == 1 { '1' } else { '0' });
        n /= 2;
    }
    digit.iter().rev().collect()
}

fn main() {
    println!("maks_dan_posisi = {:?}", maks_dan_posisi(&[4, 9, 2, 9, 1])); // Some((9, 1))
    println!("jumlah = {}", jumlah(&[1, 2, 3]));
    let mut a = [10, 20, 30];
    tukar(&mut a, 0, 2);
    println!("setelah tukar = {:?}", a); // [30, 20, 10]
    let prima: Vec<u64> = (0..30).filter(|&n| is_prima(n)).collect();
    println!("prima < 30 = {:?}", prima);
    println!("ke_biner(13) = {}", ke_biner(13)); // 1101
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uji_mudah() {
        assert_eq!(maks_dan_posisi(&[4, 9, 2, 9, 1]), Some((9, 1)));
        assert_eq!(maks_dan_posisi(&[-8, -2, -5]), Some((-2, 1)));
        assert_eq!(maks_dan_posisi(&[]), None);
        assert_eq!(jumlah(&[]), 0);
        assert_eq!(jumlah(&[i32::MAX, i32::MAX]), 2 * i32::MAX as i64);
        let mut a = [10, 20, 30];
        tukar(&mut a, 0, 2);
        assert_eq!(a, [30, 20, 10]);
        a.swap(0, 2); // fungsi bawaan
        assert_eq!(a, [10, 20, 30]);
        let prima: Vec<u64> = (0..30).filter(|&n| is_prima(n)).collect();
        assert_eq!(prima, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
        assert!(is_prima(97) && !is_prima(91) && !is_prima(1));
        for n in 0..300u64 {
            assert_eq!(ke_biner(n), format!("{:b}", n));
        }
    }
}
