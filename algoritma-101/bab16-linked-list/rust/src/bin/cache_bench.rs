// Bab 16: menjumlahkan n bilangan dari Vec dan dari LinkedList bawaan.
// Jalankan: cargo run --release --bin cache_bench. Angka bergantung mesin.
use std::collections::LinkedList;
use std::hint::black_box;
use std::time::Instant;

fn median<F: FnMut() -> u64>(mut f: F) -> f64 {
    let mut t = Vec::new();
    for _ in 0..5 {
        let s = Instant::now();
        black_box(f());
        t.push(s.elapsed().as_secs_f64());
    }
    t.sort_by(|a, b| a.partial_cmp(b).unwrap());
    t[2]
}

// Linked list berbasis indeks: node ke-i menyimpan value[i] dan next[i].
// Urutan kunjungan ditentukan next, sehingga letak node di memori bisa diatur.
fn sum_by_next(value: &[u64], next: &[usize], head: usize) -> u64 {
    let mut t = 0;
    let mut p = head;
    while p != usize::MAX {
        t += value[p];
        p = next[p];
    }
    t
}

// next untuk urutan kunjungan `order` (permutasi 0..n)
fn build_next(order: &[usize]) -> Vec<usize> {
    let mut next = vec![usize::MAX; order.len()];
    for w in order.windows(2) {
        next[w[0]] = w[1];
    }
    next
}

fn shuffled(n: usize, seed: &mut u64) -> Vec<usize> {
    let mut v: Vec<usize> = (0..n).collect();
    for i in (1..n).rev() {
        *seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let j = ((*seed >> 33) as usize) % (i + 1);
        v.swap(i, j);
    }
    v
}

fn main() {
    for n in [1_000_000u64, 10_000_000] {
        let v: Vec<u64> = (0..n).collect();
        let l: LinkedList<u64> = (0..n).collect();
        let expect = n * (n - 1) / 2;
        assert_eq!(v.iter().sum::<u64>(), expect);
        assert_eq!(l.iter().sum::<u64>(), expect);
        let tv = median(|| black_box(&v).iter().sum());
        let tl = median(|| black_box(&l).iter().sum());
        println!("n={:>9}  Vec {:.5} s  LinkedList {:.5} s  rasio {:.1}x", n, tv, tl, tl / tv);

        // node yang sama, dikunjungi berurutan di memori vs acak di memori
        let value: Vec<u64> = (0..n).collect();
        let seq: Vec<usize> = (0..n as usize).collect();
        let mut seed = 16u64;
        let rnd = shuffled(n as usize, &mut seed);
        let next_seq = build_next(&seq);
        let next_rnd = build_next(&rnd);
        assert_eq!(sum_by_next(&value, &next_rnd, rnd[0]), expect);
        let ts = median(|| sum_by_next(black_box(&value), &next_seq, seq[0]));
        let tr = median(|| sum_by_next(black_box(&value), &next_rnd, rnd[0]));
        println!("            node berurutan {:.5} s  node acak {:.5} s  rasio {:.1}x", ts, tr, tr / ts);
    }
    println!("semua uji lolos");
}
