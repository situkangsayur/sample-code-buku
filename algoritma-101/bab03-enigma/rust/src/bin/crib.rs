// Bab 3: menempatkan crib. Posisi yang membuat huruf crib berimpit dengan
// huruf yang sama di ciphertext pasti salah, karena Enigma tidak pernah
// menyandikan huruf menjadi dirinya sendiri.

fn posisi_mungkin(sandi: &[u8], crib: &[u8]) -> Vec<usize> {
    let mut hasil = Vec::new();
    for i in 0..=(sandi.len() - crib.len()) {
        let bentrok = (0..crib.len()).any(|j| sandi[i + j] == crib[j]);
        if !bentrok {
            hasil.push(i);
        }
    }
    hasil
}

fn main() {
    // Ciphertext dari enigma.py (rotor II-IV-V, cincin BUL, posisi RTZ, 10 kabel).
    let sandi = b"BTHSJLVHFNLGRLBWUQYFTENUTNCHKKILBLBOLJFG";
    let crib = b"WETTERVORHERSAGE";
    let p = posisi_mungkin(sandi, crib);
    println!("{} dari {} posisi tersisa: {:?}", p.len(), sandi.len() - crib.len() + 1, p);
    assert_eq!(p, vec![2, 3, 5, 8, 9, 10, 12, 13, 14, 16, 19, 23, 24]);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bentrok_disingkirkan() {
        assert_eq!(posisi_mungkin(b"ABCD", b"BC"), vec![0, 2]);
    }
}
