// Kode 6.15: banyak permintaan HTTP bersamaan dengan Tokio.
// Jalankan: cargo run --release [URL] [jumlah]
// Bagian kedua menunjukkan spawn_blocking untuk kerja CPU agar executor tidak tertahan.
use std::time::Instant;

#[tokio::main] // runtime multi-thread
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    let url = args.get(1).cloned().unwrap_or_else(|| "https://example.com".to_string());
    let n: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(50);

    let t0 = Instant::now();
    let mut tugas = Vec::new();
    for _ in 0..n {
        let u = url.clone();
        // spawn: future dijadwalkan di thread pool Tokio
        tugas.push(tokio::spawn(async move {
            reqwest::get(u).await.map(|r| r.status())
        }));
    }
    let mut sukses = 0;
    for t in tugas {
        if let Ok(Ok(s)) = t.await {
            if s.is_success() {
                sukses += 1;
            }
        }
    }
    println!("{sukses}/{n} sukses dalam {:?}", t0.elapsed());

    // kerja CPU berat: pindahkan ke thread blocking, bukan di dalam future biasa
    let jumlah = tokio::task::spawn_blocking(|| (0..50_000_000u64).map(|i| i % 7).sum::<u64>())
        .await
        .unwrap();
    println!("hasil kerja CPU: {jumlah}");
}
