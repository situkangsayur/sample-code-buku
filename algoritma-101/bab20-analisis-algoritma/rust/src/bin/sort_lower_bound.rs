// Bab 20: batas bawah ceil(log2 n!) dibandingkan dengan worst case merge sort
// atas semua permutasi, dan banyak perbandingan slice::sort_by bawaan Rust.
use std::cell::Cell;

fn merge_sort_count(a: &[u32]) -> (Vec<u32>, u64) {
    if a.len() <= 1 {
        return (a.to_vec(), 0);
    }
    let mid = a.len() / 2;
    let (l, cl) = merge_sort_count(&a[..mid]);
    let (r, cr) = merge_sort_count(&a[mid..]);
    let (mut out, mut i, mut j, mut c) = (Vec::with_capacity(a.len()), 0, 0, cl + cr);
    while i < l.len() && j < r.len() {
        c += 1;
        if l[i] <= r[j] { out.push(l[i]); i += 1; } else { out.push(r[j]); j += 1; }
    }
    out.extend_from_slice(&l[i..]);
    out.extend_from_slice(&r[j..]);
    (out, c)
}

fn lower_bound(n: u32) -> u32 {
    let lf: f64 = (1..=n).map(|k| (k as f64).log2()).sum();
    lf.ceil() as u32
}

// Algoritma Heap untuk membangkitkan semua permutasi
fn worst_merge(n: usize) -> u64 {
    let mut a: Vec<u32> = (0..n as u32).collect();
    let mut c = vec![0usize; n];
    let mut worst = merge_sort_count(&a).1;
    let mut i = 0;
    while i < n {
        if c[i] < i {
            if i % 2 == 0 { a.swap(0, i); } else { a.swap(c[i], i); }
            worst = worst.max(merge_sort_count(&a).1);
            c[i] += 1;
            i = 0;
        } else {
            c[i] = 0;
            i += 1;
        }
    }
    worst
}

fn count_sort_by(mut v: Vec<u32>) -> u64 {
    let count = Cell::new(0u64);
    v.sort_by(|x, y| { count.set(count.get() + 1); x.cmp(y) });
    assert!(v.windows(2).all(|w| w[0] <= w[1]));
    count.get()
}

fn main() {
    for n in 1..=8usize {
        let lb = lower_bound(n as u32);
        let wm = worst_merge(n);
        assert!(lb as u64 <= wm);
        println!("n={} ceil(log2 n!)={} merge(worst)={}", n, lb, wm);
    }
    let n = 1000u32;
    let sorted: Vec<u32> = (0..n).collect();
    let reversed: Vec<u32> = (0..n).rev().collect();
    // pengacak LCG sederhana agar tidak butuh crate luar
    let mut shuffled = sorted.clone();
    let mut state: u64 = 20;
    for i in (1..shuffled.len()).rev() {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let j = (state >> 33) as usize % (i + 1);
        shuffled.swap(i, j);
    }
    let (cs, cr, ca) = (count_sort_by(sorted), count_sort_by(reversed), count_sort_by(shuffled));
    assert!(ca >= lower_bound(n) as u64);
    println!("sort_by n={}: terurut {}, terbalik {}, acak {}, ceil(log2 n!) = {}",
             n, cs, cr, ca, lower_bound(n));
    println!("sort_lower_bound: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn small_table() {
        let expect = [(1, 0, 0), (2, 1, 1), (3, 3, 3), (4, 5, 5), (5, 7, 8), (6, 10, 11)];
        for (n, lb, wm) in expect {
            assert_eq!(lower_bound(n), lb);
            assert_eq!(worst_merge(n as usize), wm);
        }
    }
}
