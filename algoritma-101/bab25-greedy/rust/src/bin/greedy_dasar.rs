// Koin, activity selection, fractional knapsack (Algoritma 25.2-22.3).

fn koin_greedy(pecahan: &[u64], mut x: u64) -> Option<Vec<u64>> {
    let mut hasil = Vec::new();
    for &c in pecahan {
        while x >= c {
            x -= c;
            hasil.push(c);
        }
    }
    if x == 0 { Some(hasil) } else { None }
}

fn activity_selection(k: &[(&'static str, u32, u32)]) -> Vec<&'static str> {
    let mut urut = k.to_vec();
    urut.sort_by_key(|a| a.2); // urut waktu selesai
    let mut terpilih = Vec::new();
    let mut akhir = 0;
    for (nama, s, f) in urut {
        if s >= akhir {
            terpilih.push(nama);
            akhir = f;
        }
    }
    terpilih
}

fn fractional_knapsack(berat: &[u32], nilai: &[u32], w: u32) -> f64 {
    let mut idx: Vec<usize> = (0..berat.len()).collect();
    // rasio menurun: bandingkan v_i * b_j dengan v_j * b_i (tanpa pembagian)
    idx.sort_by(|&i, &j| (nilai[j] * berat[i]).cmp(&(nilai[i] * berat[j])));
    let mut sisa = w as f64;
    let mut total = 0.0;
    for i in idx {
        if sisa <= 0.0 {
            break;
        }
        let x = (sisa / berat[i] as f64).min(1.0);
        total += x * nilai[i] as f64;
        sisa -= x * berat[i] as f64;
    }
    total
}

fn main() {
    let rupiah = [50000, 20000, 10000, 5000, 2000, 1000];
    assert_eq!(koin_greedy(&rupiah, 87000), Some(vec![50000, 20000, 10000, 5000, 2000]));
    assert_eq!(koin_greedy(&[4, 3, 1], 6), Some(vec![4, 1, 1]));
    assert_eq!(koin_greedy(&[5, 2], 6), None);

    let k = [("K1", 8, 10), ("K2", 9, 11), ("K3", 10, 12), ("K4", 11, 13),
             ("K5", 8, 13), ("K6", 12, 14), ("K7", 13, 15), ("K8", 14, 16)];
    assert_eq!(activity_selection(&k), vec!["K1", "K3", "K6", "K8"]);

    let total = fractional_knapsack(&[5, 4, 6, 3], &[10, 40, 30, 50], 10);
    assert!((total - 105.0).abs() < 1e-9);
    println!("greedy_dasar: semua uji lolos");
}
