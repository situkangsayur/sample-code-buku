// Bab 1: linear search dan binary search pada 10.000 nama.
// Indeks Rust mulai dari 0; pseudocode di buku mulai dari 1.

fn linear_search(daftar: &[String], x: &str) -> (Option<usize>, u32) {
    let mut langkah = 0;
    for (i, nama) in daftar.iter().enumerate() {
        langkah += 1;
        if nama == x {
            return (Some(i), langkah);
        }
    }
    (None, langkah)
}

fn binary_search(daftar: &[String], x: &str) -> (Option<usize>, u32) {
    // lo dan hi bertipe i64 agar hi = mid - 1 tidak underflow saat mid = 0
    let (mut lo, mut hi) = (0i64, daftar.len() as i64 - 1);
    let mut langkah = 0;
    while lo <= hi {
        let mid = (lo + hi) / 2;
        langkah += 1;
        let m = &daftar[mid as usize];
        if m == x {
            return (Some(mid as usize), langkah);
        } else if m.as_str() < x {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    (None, langkah)
}

fn buat_nama(n: usize) -> Vec<String> {
    // Acakan sederhana tanpa crate luar: permutasi dengan langkah 7919 (prima, relatif prima dengan n).
    (0..n).map(|i| format!("MHS{:05}", (i * 7919) % n + 1)).collect()
}

fn main() {
    let n = 10_000;
    let acak = buat_nama(n);
    let mut urut = acak.clone();
    urut.sort();

    let (_, lin) = linear_search(&acak, "MHS99999");
    let terburuk = urut.iter().map(|x| binary_search(&urut, x).1).max().unwrap();
    println!("linear, terburuk: {} perbandingan", lin);
    println!("binary, terburuk: {} perbandingan", terburuk);
    assert_eq!(lin, 10_000);
    assert!(terburuk <= 14);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn menemukan_semua_nama() {
        let acak = buat_nama(1000);
        let mut urut = acak.clone();
        urut.sort();
        for x in &urut {
            let (i, _) = binary_search(&urut, x);
            assert_eq!(&urut[i.unwrap()], x);
            let (j, _) = linear_search(&acak, x);
            assert_eq!(&acak[j.unwrap()], x);
        }
        assert_eq!(binary_search(&urut, "TIDAK").0, None);
    }
}
