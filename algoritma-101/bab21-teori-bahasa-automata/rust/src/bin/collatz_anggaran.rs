// Menjalankan iterasi Collatz dengan anggaran langkah (Kode 21.3).

#[derive(Debug, PartialEq)]
enum Hasil {
    Berhenti(u64),
    BelumTahu(u64),
}

fn jalankan_collatz(mut n: u64, anggaran: u64) -> Hasil {
    let mut langkah = 0;
    while n != 1 {
        if langkah == anggaran {
            return Hasil::BelumTahu(langkah);
        }
        n = if n % 2 == 0 { n / 2 } else { 3 * n + 1 };
        langkah += 1;
    }
    Hasil::Berhenti(langkah)
}

fn main() {
    println!("{:?}", jalankan_collatz(27, 50)); // BelumTahu(50)
    println!("{:?}", jalankan_collatz(27, 200)); // Berhenti(111)
    assert_eq!(jalankan_collatz(6, 100), Hasil::Berhenti(8));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn batas() {
        assert_eq!(jalankan_collatz(27, 111), Hasil::Berhenti(111));
        assert_eq!(jalankan_collatz(27, 110), Hasil::BelumTahu(110));
    }
}
