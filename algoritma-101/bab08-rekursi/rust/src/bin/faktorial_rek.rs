// Algoritma 8.1 FaktorialRek di Rust (u128 agar 30! masih muat).
// Rekursi yang terlalu dalam di Rust tidak dicegat seperti RecursionError di Python:
// program berhenti dengan pesan stack overflow. Ukuran stack thread bawaan 2 MiB
// dapat diubah dengan std::thread::Builder::stack_size.
fn faktorial_rek(n: u32) -> u128 {
    if n == 0 {
        1 // kasus basis
    } else {
        n as u128 * faktorial_rek(n - 1) // langkah rekursif
    }
}

fn kedalaman(n: u64) -> u64 {
    if n == 0 { 0 } else { 1 + kedalaman(n - 1) }
}

fn main() {
    assert_eq!(faktorial_rek(4), 24);
    assert_eq!(faktorial_rek(30), 265_252_859_812_191_058_636_308_480_000_000);
    // rekursi sedalam 100.000 di thread dengan stack 64 MiB
    let h = std::thread::Builder::new()
        .stack_size(64 * 1024 * 1024)
        .spawn(|| kedalaman(100_000))
        .unwrap();
    assert_eq!(h.join().unwrap(), 100_000);
    println!("faktorial_rek: semua uji lolos");
}
