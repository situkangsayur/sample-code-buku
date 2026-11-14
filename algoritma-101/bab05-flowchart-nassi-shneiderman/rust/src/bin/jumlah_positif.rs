// Kode 5.2: JumlahPositif (Algoritma 5.3). Indeks k bertipe usize dan mulai dari 0.
fn jumlah_positif(deret: &[i64]) -> i64 {
    let mut total = 0;
    let mut k = 0;
    let mut x = deret[k]; // priming read
    while x != 0 {
        if x > 0 {
            total += x;
        }
        k += 1;
        x = deret[k]; // baca x berikutnya
    }
    total
}

fn main() {
    assert_eq!(jumlah_positif(&[5, -3, 4, 0]), 9);
    assert_eq!(jumlah_positif(&[0]), 0);
    println!("jumlah_positif: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn hanya_negatif() {
        assert_eq!(jumlah_positif(&[-1, -2, 0]), 0);
    }
    #[test]
    #[should_panic]
    fn tanpa_nol_panic() {
        jumlah_positif(&[1, 2]);
    }
}
