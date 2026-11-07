// Pola fork-join dan map-reduce dengan Rayon (work stealing).
// Jalankan: cargo run --release -- 20000000
use rayon::prelude::*;
use std::time::Instant;

// Fork-join: merge sort paralel. rayon::join menaruh salah satu cabang
// di deque worker; worker lain yang menganggur boleh mencurinya.
fn merge_sort_par(v: &mut [u64], buf: &mut [u64]) {
    const AMBANG: usize = 4096; // di bawah ini serial: task terlalu kecil merugi
    if v.len() <= AMBANG {
        v.sort_unstable();
        return;
    }
    let mid = v.len() / 2;
    let (kiri, kanan) = v.split_at_mut(mid);
    let (bkiri, bkanan) = buf.split_at_mut(mid);
    rayon::join(|| merge_sort_par(kiri, bkiri), || merge_sort_par(kanan, bkanan));
    gabung(kiri, kanan, buf);
    v.copy_from_slice(buf);
}

fn gabung(a: &[u64], b: &[u64], out: &mut [u64]) {
    let (mut i, mut j, mut k) = (0, 0, 0);
    while i < a.len() && j < b.len() {
        if a[i] <= b[j] { out[k] = a[i]; i += 1; } else { out[k] = b[j]; j += 1; }
        k += 1;
    }
    out[k..k + a.len() - i].copy_from_slice(&a[i..]);
    k += a.len() - i;
    out[k..].copy_from_slice(&b[j..]);
}

fn main() {
    let n: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(10_000_000);
    // data acak sederhana (xorshift) agar tanpa dependensi tambahan
    let mut x: u64 = 88172645463325252;
    let mut data: Vec<u64> = (0..n).map(|_| { x ^= x << 13; x ^= x >> 7; x ^= x << 17; x % 1_000_000 }).collect();

    // Map-reduce: jumlah kuadrat, dipecah otomatis oleh par_iter
    let t = Instant::now();
    let jumlah: u128 = data.par_iter().map(|&v| (v as u128) * (v as u128)).sum();
    println!("map-reduce: jumlah kuadrat = {jumlah} ({:?})", t.elapsed());

    let mut serial = data.clone();
    let t = Instant::now();
    serial.sort_unstable();
    println!("sort serial  : {:?}", t.elapsed());

    let mut buf = vec![0u64; n];
    let t = Instant::now();
    merge_sort_par(&mut data, &mut buf);
    println!("merge sort par: {:?} dengan {} thread", t.elapsed(), rayon::current_num_threads());
    assert_eq!(data, serial, "hasil paralel harus sama dengan serial");

    // Pembanding library: par_sort_unstable dari Rayon (penggabungan juga diparalelkan)
    let mut lagi = serial.clone();
    lagi.reverse();
    let t = Instant::now();
    lagi.par_sort_unstable();
    println!("par_sort_unstable: {:?}", t.elapsed());
    println!("LULUS");
}
