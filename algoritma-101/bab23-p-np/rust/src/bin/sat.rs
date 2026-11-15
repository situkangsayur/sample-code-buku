// Verifikasi dan brute force SAT (Algoritma 23.1 dan 29.2, Kode 23.2).
// Literal k > 0 berarti x_k, -k berarti (not x_k). nilai[0] tidak dipakai.

fn verifikasi_sat(klausa: &[Vec<i32>], nilai: &[bool]) -> bool {
    klausa.iter().all(|c| {
        c.iter().any(|&lit| {
            let v = nilai[lit.unsigned_abs() as usize];
            if lit > 0 { v } else { !v }
        })
    })
}

fn brute_force_sat(klausa: &[Vec<i32>], n: usize) -> Option<(Vec<bool>, u64)> {
    for mask in 0u64..(1u64 << n) {
        let mut nilai = vec![false; n + 1];
        for i in 0..n {
            nilai[i + 1] = (mask >> i) & 1 == 1;
        }
        if verifikasi_sat(klausa, &nilai) {
            return Some((nilai, mask + 1));
        }
    }
    None
}

fn main() {
    let phi = vec![vec![1, 2], vec![-2, 3], vec![-1, -2], vec![2, 3]];
    println!("{}", verifikasi_sat(&phi, &[false, true, false, true])); // true
    println!("{}", verifikasi_sat(&phi, &[false, true, true, true])); // false
    if let Some((nilai, coba)) = brute_force_sat(&phi, 3) {
        println!("{:?} {}", &nilai[1..], coba); // [true, false, true] 6
    }
    assert!(brute_force_sat(&[vec![1], vec![-1]], 1).is_none());
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn klausa_kosong_gagal() {
        assert!(!verifikasi_sat(&[vec![]], &[false]));
    }
    #[test]
    fn solusi_pertama() {
        let phi = vec![vec![1, 2], vec![-2, 3], vec![-1, -2], vec![2, 3]];
        let (nilai, coba) = brute_force_sat(&phi, 3).unwrap();
        assert_eq!(&nilai[1..], &[true, false, true]);
        assert_eq!(coba, 6);
    }
}
