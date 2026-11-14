// Algoritma 8.2 Hanoi di Rust. Tidak ada indeks, jadi tidak ada pergeseran 0/1.
fn hanoi(n: u32, asal: char, tujuan: char, bantu: char, langkah: &mut Vec<(u32, char, char)>) {
    if n > 0 {
        hanoi(n - 1, asal, bantu, tujuan, langkah);
        langkah.push((n, asal, tujuan));
        hanoi(n - 1, bantu, tujuan, asal, langkah);
    }
}

fn main() {
    let mut langkah = Vec::new();
    hanoi(3, 'A', 'C', 'B', &mut langkah);
    for (i, (n, a, t)) in langkah.iter().enumerate() {
        println!("{}. cakram {}: {} -> {}", i + 1, n, a, t);
    }
    assert_eq!(langkah.len(), 7);
    assert_eq!(langkah[3], (3, 'A', 'C'));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn dua_pangkat_n_kurang_satu() {
        for n in 0..15 {
            let mut l = Vec::new();
            hanoi(n, 'A', 'C', 'B', &mut l);
            assert_eq!(l.len(), (1usize << n) - 1);
        }
    }
}
