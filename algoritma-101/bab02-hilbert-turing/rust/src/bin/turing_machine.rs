// Bab 2: simulator Turing machine satu pita.
use std::collections::HashMap;

const KOSONG: char = '_';

#[derive(Clone, Copy)]
enum Arah {
    Kiri,
    Kanan,
}

// (state, simbol) -> (state baru, simbol ditulis, arah)
type Tabel = HashMap<(&'static str, char), (&'static str, char, Arah)>;

fn tambah_satu() -> Tabel {
    use Arah::*;
    HashMap::from([
        (("kanan", '0'), ("kanan", '0', Kanan)),
        (("kanan", '1'), ("kanan", '1', Kanan)),
        (("kanan", KOSONG), ("bawa", KOSONG, Kiri)),
        (("bawa", '1'), ("bawa", '0', Kiri)),
        (("bawa", '0'), ("selesai", '1', Kiri)),
        (("bawa", KOSONG), ("selesai", '1', Kiri)),
    ])
}

/// Mengembalikan (isi pita, banyak langkah, berhenti?).
fn jalankan(tabel: &Tabel, awal: &str, mut state: &'static str, henti: &str, batas: u64) -> (String, u64, bool) {
    // Pita sebagai HashMap posisi -> simbol, agar bisa tumbuh ke kiri (posisi negatif).
    let mut pita: HashMap<i64, char> = awal.chars().enumerate().map(|(i, c)| (i as i64, c)).collect();
    let (mut kepala, mut langkah) = (0i64, 0u64);
    while state != henti {
        if langkah >= batas {
            return (isi(&pita), langkah, false);
        }
        let dibaca = *pita.get(&kepala).unwrap_or(&KOSONG);
        let Some(&(baru, tulis, arah)) = tabel.get(&(state, dibaca)) else { break };
        pita.insert(kepala, tulis);
        kepala += match arah { Arah::Kiri => -1, Arah::Kanan => 1 };
        state = baru;
        langkah += 1;
    }
    (isi(&pita), langkah, true)
}

fn isi(pita: &HashMap<i64, char>) -> String {
    let lo = *pita.keys().min().unwrap_or(&0);
    let hi = *pita.keys().max().unwrap_or(&-1);
    let s: String = (lo..=hi).map(|i| *pita.get(&i).unwrap_or(&KOSONG)).collect();
    s.trim_matches(KOSONG).to_string()
}

fn main() {
    let t = tambah_satu();
    let (hasil, langkah, ok) = jalankan(&t, "1011", "kanan", "selesai", 10_000);
    println!("1011 + 1 = {} dalam {} langkah", hasil, langkah); // 1100, 8
    assert_eq!((hasil.as_str(), langkah, ok), ("1100", 8, true));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tambah_satu_benar() {
        let t = tambah_satu();
        for n in 0u32..200 {
            let (h, _, ok) = jalankan(&t, &format!("{:b}", n), "kanan", "selesai", 10_000);
            assert!(ok);
            assert_eq!(u32::from_str_radix(&h, 2).unwrap(), n + 1);
        }
    }

    #[test]
    fn mesin_tanpa_henti_dibatasi() {
        let t: Tabel = HashMap::from([(("jalan", KOSONG), ("jalan", KOSONG, Arah::Kanan))]);
        let (_, langkah, ok) = jalankan(&t, "", "jalan", "selesai", 1000);
        assert!(!ok);
        assert_eq!(langkah, 1000);
    }
}
