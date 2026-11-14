// Bab 34: natural merge sort yang stabil (inti gagasan Timsort dan driftsort).
// Langkah: potong menjadi run naik alami, lalu gabung run berpasangan
// sampai tersisa satu. Indeks mulai 0 (Rust).

/// Batas run naik tidak tegas mulai dari indeks 0 sampai akhir.
fn cari_run<T: Ord>(a: &[T]) -> Vec<usize> {
    let mut batas = vec![0];
    for i in 1..a.len() {
        if a[i] < a[i - 1] {
            batas.push(i);
        }
    }
    batas.push(a.len());
    batas
}

/// Gabung a[lo..mid] dan a[mid..hi]; ambil kiri bila sama (stabil).
fn merge<T: Ord + Clone>(a: &mut [T], lo: usize, mid: usize, hi: usize) {
    let kiri: Vec<T> = a[lo..mid].to_vec();
    let (mut i, mut j, mut k) = (0, mid, lo);
    while i < kiri.len() && j < hi {
        if a[j] < kiri[i] {
            a[k] = a[j].clone();
            j += 1;
        } else {
            a[k] = kiri[i].clone();
            i += 1;
        }
        k += 1;
    }
    while i < kiri.len() {
        a[k] = kiri[i].clone();
        i += 1;
        k += 1;
    }
}

pub fn natural_merge_sort<T: Ord + Clone>(a: &mut [T]) -> usize {
    let mut batas = cari_run(a);
    let run_awal = batas.len() - 1;
    while batas.len() > 2 {
        let mut baru = vec![0];
        let mut r = 0;
        while r + 2 < batas.len() {
            merge(a, batas[r], batas[r + 1], batas[r + 2]);
            baru.push(batas[r + 2]);
            r += 2;
        }
        if r + 2 == batas.len() {
            baru.push(batas[r + 1]); // run ganjil terakhir ikut apa adanya
        }
        batas = baru;
    }
    run_awal
}

fn main() {
    let mut v = vec![3, 8, 9, 2, 4, 7, 1, 5, 6];
    let run = natural_merge_sort(&mut v);
    println!("{} run awal, hasil {:?}", run, v); // 3 run awal
    assert_eq!(run, 3);
    assert_eq!(v, vec![1, 2, 3, 4, 5, 6, 7, 8, 9]);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sama_dengan_sort_bawaan() {
        let mut x: u64 = 33;
        for n in [0usize, 1, 2, 7, 100, 1000] {
            let mut v: Vec<u64> = (0..n)
                .map(|_| {
                    x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
                    (x >> 33) % 50
                })
                .collect();
            let mut w = v.clone();
            natural_merge_sort(&mut v);
            w.sort();
            assert_eq!(v, w);
        }
    }

    #[test]
    fn data_terurut_satu_run() {
        let mut v: Vec<i32> = (0..500).collect();
        assert_eq!(natural_merge_sort(&mut v), 1);
    }
}
