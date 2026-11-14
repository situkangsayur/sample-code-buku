// Bab 12: bubble, selection, dan insertion sort di Rust.
// Setiap fungsi mengembalikan (jumlah perbandingan, jumlah tukar/geser).
// Jalankan: cargo run --bin sorting ; uji: cargo test --bin sorting

fn bubble_sort(a: &mut [i32]) -> (usize, usize) {
    let n = a.len();
    let (mut banding, mut tukar) = (0, 0);
    for i in 0..n.saturating_sub(1) {
        // n - 1 biasa akan underflow bila n = 0
        let mut ada_tukar = false;
        for j in 0..n - 1 - i {
            banding += 1;
            if a[j] > a[j + 1] {
                a.swap(j, j + 1);
                tukar += 1;
                ada_tukar = true;
            }
        }
        if !ada_tukar {
            break;
        }
    }
    (banding, tukar)
}

fn selection_sort(a: &mut [i32]) -> (usize, usize) {
    let n = a.len();
    let (mut banding, mut tukar) = (0, 0);
    for i in 0..n.saturating_sub(1) {
        let mut imin = i;
        for j in i + 1..n {
            banding += 1;
            if a[j] < a[imin] {
                imin = j;
            }
        }
        if imin != i {
            a.swap(i, imin);
            tukar += 1;
        }
    }
    (banding, tukar)
}

fn insertion_sort(a: &mut [i32]) -> (usize, usize) {
    let (mut banding, mut geser) = (0, 0);
    for i in 1..a.len() {
        let kunci = a[i];
        let mut j = i; // j = posisi kosong; yang dibandingkan a[j - 1]
        while j > 0 {
            banding += 1;
            if a[j - 1] > kunci {
                a[j] = a[j - 1];
                geser += 1;
                j -= 1;
            } else {
                break;
            }
        }
        a[j] = kunci;
    }
    (banding, geser)
}

fn main() {
    let contoh = [29, 10, 14, 37, 13];
    let fs: [(&str, fn(&mut [i32]) -> (usize, usize)); 3] = [
        ("bubble", bubble_sort),
        ("selection", selection_sort),
        ("insertion", insertion_sort),
    ];
    for (nama, f) in fs {
        let mut b = contoh;
        let hasil = f(&mut b);
        println!("{:<10} {:?} banding/tukar-geser = {:?}", nama, b, hasil);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const SEMUA: [fn(&mut [i32]) -> (usize, usize); 3] =
        [bubble_sort, selection_sort, insertion_sort];

    #[test]
    fn angka_tabel_buku() {
        assert_eq!(bubble_sort(&mut [29, 10, 14, 37, 13]), (10, 5));
        assert_eq!(selection_sort(&mut [29, 10, 14, 37, 13]), (10, 3));
        assert_eq!(insertion_sort(&mut [29, 10, 14, 37, 13]), (8, 5));
        assert_eq!(bubble_sort(&mut [1, 2, 3, 4, 5]), (4, 0));
        assert_eq!(insertion_sort(&mut [5, 4, 3, 2, 1]), (10, 10));
    }

    #[test]
    fn kasus_batas() {
        let kasus: Vec<Vec<i32>> = vec![
            vec![],
            vec![7],
            vec![2, 1],
            vec![1, 2, 3, 4, 5],
            vec![5, 4, 3, 2, 1],
            vec![3, 3, 3, 3],
            vec![4, 1, 4, 1, 4],
            vec![0, -5, 12, -5, 7],
            vec![i32::MAX, i32::MIN, 0],
        ];
        for f in SEMUA {
            for k in &kasus {
                let mut b = k.clone();
                f(&mut b);
                let mut harap = k.clone();
                harap.sort();
                assert_eq!(b, harap);
            }
        }
    }

    #[test]
    fn uji_acak() {
        let mut s: u64 = 12;
        let mut acak = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (s >> 33) as i32
        };
        for _ in 0..3000 {
            let n = (acak() % 31) as usize;
            let a: Vec<i32> = (0..n).map(|_| acak() % 101 - 50).collect();
            let mut harap = a.clone();
            harap.sort();
            for f in SEMUA {
                let mut b = a.clone();
                f(&mut b);
                assert_eq!(b, harap);
            }
        }
    }
}
