//! Pelatihan dan penerapan aturan merge BPE dari nol (tanpa crate), padanan bpe_dari_nol.py.
use std::collections::HashMap;

type Kosakata = Vec<(Vec<String>, u32)>;

fn hitung_pasangan(kosa: &Kosakata) -> Vec<((String, String), u32)> {
    // Simpan urutan kemunculan pertama agar seri dipecahkan seperti versi Python.
    let mut urutan: Vec<(String, String)> = Vec::new();
    let mut hitung: HashMap<(String, String), u32> = HashMap::new();
    for (simbol, frek) in kosa {
        for w in simbol.windows(2) {
            let p = (w[0].clone(), w[1].clone());
            if !hitung.contains_key(&p) { urutan.push(p.clone()); }
            *hitung.entry(p).or_insert(0) += frek;
        }
    }
    urutan.into_iter().map(|p| { let n = hitung[&p]; (p, n) }).collect()
}

fn gabung(p: &(String, String), simbol: &[String]) -> Vec<String> {
    let mut hasil = Vec::new();
    let mut i = 0;
    while i < simbol.len() {
        if i + 1 < simbol.len() && simbol[i] == p.0 && simbol[i + 1] == p.1 {
            hasil.push(format!("{}{}", p.0, p.1));
            i += 2;
        } else {
            hasil.push(simbol[i].clone());
            i += 1;
        }
    }
    hasil
}

fn pecah(kata: &str) -> Vec<String> {
    let mut s: Vec<String> = kata.chars().map(|c| c.to_string()).collect();
    s.push("_".to_string());
    s
}

fn main() {
    let korpus = [("makan", 6), ("makanan", 4), ("dimakan", 3), ("minum", 3), ("minuman", 2)];
    let mut kosa: Kosakata = korpus.iter().map(|(k, f)| (pecah(k), *f)).collect();
    let mut aturan: Vec<(String, String)> = Vec::new();
    for langkah in 1..=7 {
        let pasangan = hitung_pasangan(&kosa);
        let maks = pasangan.iter().map(|(_, n)| *n).max().unwrap();
        let (terbaik, n) = pasangan.into_iter().find(|(_, c)| *c == maks).unwrap();
        println!("{langkah} {:?} {n}", terbaik);
        kosa = kosa.iter().map(|(s, f)| (gabung(&terbaik, s), *f)).collect();
        aturan.push(terbaik);
    }
    for kata in ["makanan", "dimakan", "minuman", "makanlah"] {
        let mut s = pecah(kata);
        for p in &aturan { s = gabung(p, &s); }
        println!("{kata:10} -> {:?}", s);
    }
}
