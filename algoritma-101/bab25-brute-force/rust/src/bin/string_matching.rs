// String matching naif (Algoritma 25.1, versi Rust dari Kode 25.1).
fn cari_naif(teks: &[u8], pola: &[u8]) -> (Vec<usize>, usize) {
    let (n, m) = (teks.len(), pola.len());
    let mut posisi = Vec::new();
    let mut banding = 0;
    if m > n {
        return (posisi, 0);
    }
    for i in 0..=(n - m) {
        let mut j = 0;
        while j < m {
            banding += 1;
            if teks[i + j] != pola[j] {
                break;
            }
            j += 1;
        }
        if j == m {
            posisi.push(i);
        }
    }
    (posisi, banding)
}

fn main() {
    assert_eq!(cari_naif(b"ABRAKADABRA", b"ABRA"), (vec![0, 7], 16));
    let teks = vec![b'A'; 20];
    assert_eq!(cari_naif(&teks, b"AAAAB"), (vec![], 16 * 5));
    println!("string_matching: semua uji lolos");
}
