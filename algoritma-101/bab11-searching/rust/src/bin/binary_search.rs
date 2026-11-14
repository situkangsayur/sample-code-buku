// Bab 11: binary search di Rust dengan ruang [lo, hi) setengah terbuka.
// Indeks usize tidak boleh negatif, jadi hi = mid (bukan mid - 1) menghindari underflow.

fn binary_search(a: &[i32], x: i32) -> Option<usize> {
    let mut lo = 0;
    let mut hi = a.len(); // hi menunjuk satu posisi sesudah elemen terakhir
    while lo < hi {
        let mid = lo + (hi - lo) / 2; // tidak overflow
        if a[mid] == x {
            return Some(mid);
        } else if a[mid] < x {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    None
}

/// Rumus tengah yang naif. Dengan i32, lo + hi dapat melewati i32::MAX.
/// Hanya dipakai di uji (#[should_panic]), maka dead_code diizinkan.
#[allow(dead_code)]
fn tengah_naif(lo: i32, hi: i32) -> i32 {
    (lo + hi) / 2
}

fn tengah_aman(lo: i32, hi: i32) -> i32 {
    lo + (hi - lo) / 2
}

fn main() {
    let a = [3, 8, 15, 21, 27, 34, 42, 50, 61, 77];
    println!("cari 42 -> {:?}", binary_search(&a, 42)); // Some(6)
    println!("cari 20 -> {:?}", binary_search(&a, 20)); // None
    println!("bawaan  -> {:?}", a.binary_search(&20)); // Err(3): posisi sisip
    let (lo, hi) = (1_500_000_000, 2_000_000_000);
    println!("tengah_aman = {}", tengah_aman(lo, hi)); // 1750000000
    println!("(lo + hi) dengan wrapping = {}", lo.wrapping_add(hi)); // negatif
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uji_binary() {
        let a = [3, 8, 15, 21, 27, 34, 42, 50, 61, 77];
        for (i, &v) in a.iter().enumerate() {
            assert_eq!(binary_search(&a, v), Some(i));
        }
        for x in [0, 1, 20, 22, 78, 100] {
            assert_eq!(binary_search(&a, x), None);
        }
        assert_eq!(binary_search(&[], 5), None);
        assert_eq!(binary_search(&[5], 5), Some(0));
        assert_eq!(binary_search(&[5], 4), None); // kasus yang membuat hi = mid - 1 underflow
        assert_eq!(tengah_aman(1_500_000_000, 2_000_000_000), 1_750_000_000);
    }

    #[test]
    fn uji_acak_terhadap_bawaan() {
        // pembangkit acak sederhana (LCG) agar tidak butuh crate tambahan
        let mut s: u64 = 2026;
        let mut acak = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (s >> 33) as i32
        };
        for _ in 0..2000 {
            let n = (acak() % 40) as usize;
            let mut v: Vec<i32> = (0..n).map(|_| acak() % 200).collect();
            v.sort();
            v.dedup();
            let x = acak() % 210 - 5;
            assert_eq!(binary_search(&v, x).is_some(), v.binary_search(&x).is_ok());
            if let Some(i) = binary_search(&v, x) {
                assert_eq!(v[i], x);
            }
        }
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn tengah_naif_overflow() {
        let lo = std::hint::black_box(1_500_000_000);
        let hi = std::hint::black_box(2_000_000_000);
        tengah_naif(lo, hi);
    }
}
