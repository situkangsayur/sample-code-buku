// Bab 10: padanan pseudocode dan Rust.
// Pseudocode memakai indeks mulai 1, Rust mulai 0.
// Jalankan: cargo run --bin padanan ; uji: cargo test --bin padanan

/// Algoritma Maksimum: nilai terbesar di slice a (tidak kosong).
fn maksimum(a: &[i64]) -> i64 {
    let mut maks = a[0]; // pseudocode: maks <- A[1]
    for i in 1..a.len() {
        // pseudocode: for i <- 2 to n
        if a[i] > maks {
            maks = a[i];
        }
    }
    maks
}

/// Jumlah 1 + 2 + ... + n. Range 1..=n memuat n.
fn jumlah_deret(n: u64) -> u64 {
    let mut s = 0;
    for i in 1..=n {
        s += i;
    }
    s
}

/// FPB Euclid dengan while.
fn fpb(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

/// Faktorial rekursif. u128 cukup sampai 34!.
fn faktorial(n: u32) -> u128 {
    if n == 0 {
        1
    } else {
        n as u128 * faktorial(n - 1)
    }
}

/// Padanan repeat ... until x > 0 dengan loop + break.
fn baca_sampai_positif(data: &[i32]) -> i32 {
    let mut i = 0;
    let x = loop {
        let x = data[i]; // badan loop: minimal sekali
        i += 1;
        if x > 0 {
            break x; // loop dapat mengembalikan nilai lewat break
        }
    };
    x
}

/// Padanan case dengan match. Semua kemungkinan wajib ditangani.
fn nama_hari(k: u32) -> &'static str {
    match k {
        1 => "Senin",
        2 => "Selasa",
        6 | 7 => "akhir pekan",
        _ => "hari kerja lain",
    }
}

fn main() {
    println!("maksimum = {}", maksimum(&[7, 3, 9, 2])); // 9
    println!("jumlah_deret(100) = {}", jumlah_deret(100)); // 5050
    println!("fpb(48, 18) = {}", fpb(48, 18)); // 6
    println!("faktorial(30) = {}", faktorial(30));
    println!("nama_hari(6) = {}", nama_hari(6));
    println!("repeat-until: {}", baca_sampai_positif(&[-3, 0, 4, 8])); // 4
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uji_padanan() {
        assert_eq!(maksimum(&[7, 3, 9, 2]), 9);
        assert_eq!(maksimum(&[-5]), -5);
        assert_eq!(jumlah_deret(100), 5050);
        assert_eq!(jumlah_deret(0), 0);
        assert_eq!(fpb(48, 18), 6);
        assert_eq!(fpb(17, 5), 1);
        assert_eq!(faktorial(5), 120);
        assert_eq!(faktorial(30), 265252859812191058636308480000000);
        assert_eq!(baca_sampai_positif(&[-3, 0, 4, 8]), 4);
        assert_eq!(nama_hari(1), "Senin");
        assert_eq!(nama_hari(4), "hari kerja lain");
    }
}
