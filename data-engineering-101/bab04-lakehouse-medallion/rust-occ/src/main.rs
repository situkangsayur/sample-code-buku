// Kode 4.8: commit optimistik dengan compare-and-swap (CAS) di Rust.
// Pointer katalog = AtomicU64 berisi nomor versi metadata terbaru.
// Delapan penulis menambah satu versi masing-masing; tidak ada yang hilang.
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, Barrier};
use std::thread;
use std::time::Duration;

fn commit(pointer: &AtomicU64) -> (u64, u32) {
    let mut coba = 0;
    loop {
        coba += 1;
        let dasar = pointer.load(Ordering::Acquire); // baca versi terbaru
        thread::sleep(Duration::from_micros(200)); // tulis Parquet + metadata
        let baru = dasar + 1;
        // tukar pointer hanya bila masih menunjuk versi dasar
        if pointer
            .compare_exchange(dasar, baru, Ordering::AcqRel, Ordering::Acquire)
            .is_ok()
        {
            return (baru, coba);
        } // kalah balapan: baca ulang lalu coba lagi
    }
}

fn main() {
    let pointer = Arc::new(AtomicU64::new(0));
    let mulai = Arc::new(Barrier::new(8));
    let tangan: Vec<_> = (0..8)
        .map(|p| {
            let (ptr, b) = (Arc::clone(&pointer), Arc::clone(&mulai));
            thread::spawn(move || {
                b.wait(); // semua penulis mulai bersamaan
                (p, commit(&ptr))
            })
        })
        .collect();
    for t in tangan {
        let (p, (versi, coba)) = t.join().unwrap();
        println!("penulis {p}: commit v{versi} setelah {coba} percobaan");
    }
    println!("versi akhir: {}", pointer.load(Ordering::Acquire));
}
