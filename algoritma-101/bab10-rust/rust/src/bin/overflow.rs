// Bab 10: tipe bilangan bulat dan overflow.
// cargo run --bin overflow                     (aman, keluar normal)
// cargo run --bin overflow -- panik            (profil dev: overflow-checks aktif -> panic)
// cargo run --release --bin overflow -- panik  (profil release: overflow-checks mati -> 4)
use std::hint::black_box;

/// Penjumlahan biasa. Di profil dev, overflow menyebabkan panic.
fn tambah(a: u8, b: u8) -> u8 {
    a + b
}

/// Faktorial dengan checked_mul: None bila hasil tidak muat di u64.
fn faktorial_aman(n: u64) -> Option<u64> {
    let mut hasil: u64 = 1;
    for i in 2..=n {
        hasil = hasil.checked_mul(i)?; // ? : kembalikan None bila overflow
    }
    Some(hasil)
}

fn main() {
    println!("u8   : {} .. {}", u8::MIN, u8::MAX);
    println!("i32  : {} .. {}", i32::MIN, i32::MAX);
    println!("u64  : {} .. {}", u64::MIN, u64::MAX);

    // Perilaku eksplisit, sama di dev maupun release
    println!("250u8.checked_add(10)    = {:?}", 250u8.checked_add(10)); // None
    println!("250u8.wrapping_add(10)   = {}", 250u8.wrapping_add(10)); // 4
    println!("250u8.saturating_add(10) = {}", 250u8.saturating_add(10)); // 255
    println!("250u8.overflowing_add(10)= {:?}", 250u8.overflowing_add(10)); // (4, true)
    println!("20! = {:?}, 21! = {:?}", faktorial_aman(20), faktorial_aman(21));

    if std::env::args().nth(1).as_deref() != Some("panik") {
        return; // bagian di bawah sengaja overflow; jalankan dengan argumen panik
    }
    // black_box mencegah compiler menghitung hasilnya saat kompilasi
    let a = black_box(250u8);
    let b = black_box(10u8);
    println!("menghitung 250u8 + 10u8 dengan + biasa ...");
    let c = tambah(a, b); // dev: panic; release: 4
    println!("hasil = {}", c);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn metode_eksplisit() {
        assert_eq!(250u8.checked_add(10), None);
        assert_eq!(250u8.wrapping_add(10), 4);
        assert_eq!(250u8.saturating_add(10), 255);
        assert_eq!(250u8.overflowing_add(10), (4, true));
        assert_eq!(faktorial_aman(20), Some(2432902008176640000));
        assert_eq!(faktorial_aman(21), None);
        assert_eq!(tambah(100, 55), 155);
    }

    // cargo test memakai profil test (turunan dev), jadi overflow-checks aktif
    #[test]
    #[should_panic(expected = "overflow")]
    fn tambah_overflow_panic() {
        tambah(black_box(250), black_box(10));
    }
}
