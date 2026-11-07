// Kode 9.20: menghitung pi dengan Rayon.
// RAYON_NUM_THREADS=4 cargo run --release
use rayon::prelude::*;
use std::time::Instant;

fn main() {
    let n: u64 = 1_000_000_000;
    let h = 1.0 / n as f64;
    let mulai = Instant::now();
    let jumlah: f64 = (0..n)
        .into_par_iter()
        .map(|i| {
            let x = (i as f64 + 0.5) * h;
            4.0 / (1.0 + x * x)
        })
        .sum();
    println!(
        "pi ~ {:.12}  {} thread  {:.3} s",
        jumlah * h,
        rayon::current_num_threads(),
        mulai.elapsed().as_secs_f64()
    );
}
