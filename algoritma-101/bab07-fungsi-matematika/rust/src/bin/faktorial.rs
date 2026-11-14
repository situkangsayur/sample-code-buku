// Kode 7.1: faktorial di Rust dengan pemeriksaan overflow (Algoritma 7.1).
fn faktorial(n: u64) -> Option<u64> {
    let mut hasil: u64 = 1;
    for i in 2..=n {
        hasil = hasil.checked_mul(i)?; // None bila tidak muat
    }
    Some(hasil)
}

fn main() {
    assert_eq!(faktorial(20), Some(2_432_902_008_176_640_000));
    assert_eq!(faktorial(21), None); // 21! melewati batas u64
    println!("faktorial: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn kecil() {
        assert_eq!(faktorial(0), Some(1));
        assert_eq!(faktorial(1), Some(1));
        assert_eq!(faktorial(5), Some(120));
    }
    #[test]
    fn dua_puluh_masih_muat_di_i64() {
        assert!(faktorial(20).unwrap() <= i64::MAX as u64);
    }
}
