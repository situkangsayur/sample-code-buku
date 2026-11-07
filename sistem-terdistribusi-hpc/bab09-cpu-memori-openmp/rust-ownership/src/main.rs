// Kode 9.5: ownership, borrowing, dan Arc di Rust.
use std::sync::Arc;
use std::thread;

fn main() {
    let a = vec![1, 2, 3]; // a adalah pemilik
    let b = a; // kepemilikan pindah ke b
    // println!("{:?}", a);     // DITOLAK compiler: value borrowed after move
    let r = &b; // pinjam untuk dibaca
    println!("{:?}", r);

    // Banyak pemilik antar-thread: Arc (atomic reference counting).
    let data = Arc::new(vec![1.0_f64; 1000]);
    let salinan = Arc::clone(&data);
    let h = thread::spawn(move || salinan.iter().sum::<f64>());
    println!("jumlah = {}", h.join().unwrap());
    println!("strong_count = {}", Arc::strong_count(&data));
} // b dan data dibebaskan di sini (Drop)
