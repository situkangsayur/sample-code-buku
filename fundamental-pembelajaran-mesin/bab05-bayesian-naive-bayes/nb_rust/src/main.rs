// Naive Bayes multinomial dengan Laplace smoothing, dihitung dalam log (Bab 5, Kode 5.4).
use std::collections::{HashMap, HashSet};

struct Nb { log_prior: HashMap<String, f64>, hitung: HashMap<String, HashMap<String, f64>>,
            total: HashMap<String, f64>, v: f64 }

fn latih(data: &[(&str, &str)]) -> Nb {
    let mut n_kelas: HashMap<String, f64> = HashMap::new();
    let mut hitung: HashMap<String, HashMap<String, f64>> = HashMap::new();
    let mut kosakata = HashSet::new();
    for (teks, c) in data {
        *n_kelas.entry(c.to_string()).or_insert(0.0) += 1.0;
        for w in teks.split_whitespace() {
            *hitung.entry(c.to_string()).or_default().entry(w.to_string()).or_insert(0.0) += 1.0;
            kosakata.insert(w.to_string());
        }
    }
    let n = data.len() as f64;
    let log_prior = n_kelas.iter().map(|(c, k)| (c.clone(), (k / n).ln())).collect();
    let total = hitung.iter().map(|(c, h)| (c.clone(), h.values().sum())).collect();
    Nb { log_prior, hitung, total, v: kosakata.len() as f64 }
}

fn skor(m: &Nb, teks: &str, c: &str) -> f64 {
    let penyebut = m.total[c] + m.v; // Laplace: tambah 1 untuk tiap kata kosakata
    m.log_prior[c] + teks.split_whitespace()
        .map(|w| ((m.hitung[c].get(w).copied().unwrap_or(0.0) + 1.0) / penyebut).ln())
        .sum::<f64>()
}

fn main() {
    let data = [("menang hadiah gratis", "spam"), ("gratis hadiah klik sekarang", "spam"),
                ("klik gratis menang", "spam"), ("rapat besok pagi", "bukan"),
                ("jadwal rapat proyek", "bukan"), ("kirim laporan proyek besok", "bukan")];
    let m = latih(&data);
    for surel in ["gratis klik hadiah", "gratis rapat besok"] {
        let (s, b) = (skor(&m, surel, "spam"), skor(&m, surel, "bukan"));
        let p_spam = 1.0 / (1.0 + (b - s).exp());
        println!("{surel:20} P(spam)={p_spam:.3}");
    }
}
