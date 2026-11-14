// Kode 6.2: procedure Tukar dan function CariMaks di Rust, ditambah HitungMuncul dan Balik.
fn tukar(a: &mut [i64], i: usize, j: usize) {
    let temp = a[i];
    a[i] = a[j];
    a[j] = temp;
}

fn cari_maks(a: &[i64]) -> i64 {
    let mut maks = a[0];
    for i in 1..a.len() {
        // 1..len berarti 1 sampai len-1
        if a[i] > maks {
            maks = a[i];
        }
    }
    maks
}

fn hitung_muncul(a: &[i64], x: i64, k: usize) -> usize {
    let mut c = 0;
    for &v in a {
        if !(v == x) {
            continue; // bukan x, lewati
        }
        c += 1;
        if c == k {
            break; // batas tercapai
        }
    }
    c
}

fn balik(a: &mut [i64]) {
    let n = a.len();
    for i in 0..n / 2 {
        tukar(a, i, n - 1 - i);
    }
}

fn main() {
    let mut data = vec![42, 17, 88, 63, 25];
    tukar(&mut data, 0, 2);
    assert_eq!(data, vec![88, 17, 42, 63, 25]);
    assert_eq!(cari_maks(&data), 88);
    assert_eq!(hitung_muncul(&[3, 1, 3, 3, 2, 3], 3, 2), 2);
    balik(&mut data);
    assert_eq!(data, vec![25, 63, 42, 17, 88]);
    println!("fungsi_prosedur: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn balik_ganjil_genap() {
        let mut a = vec![1, 2, 3, 4, 5, 6, 7];
        balik(&mut a);
        assert_eq!(a, vec![7, 6, 5, 4, 3, 2, 1]);
        let mut b = vec![1, 2, 3, 4];
        balik(&mut b);
        assert_eq!(b, vec![4, 3, 2, 1]);
    }
    #[test]
    fn maks_negatif() {
        assert_eq!(cari_maks(&[-5, -2, -9]), -2);
    }
    #[test]
    fn swap_bawaan_sama() {
        let mut a = vec![1, 2, 3];
        let mut b = a.clone();
        tukar(&mut a, 0, 2);
        b.swap(0, 2);
        assert_eq!(a, b);
    }
}
