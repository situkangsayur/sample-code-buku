// HashMap bawaan Rust: hitung kata dengan entry API (Kode 18.5).
use std::collections::HashMap;

fn hitung_kata(teks: &str) -> HashMap<String, usize> {
    let mut frek: HashMap<String, usize> = HashMap::new();
    for kata in teks.to_lowercase().split_whitespace() {
        *frek.entry(kata.to_string()).or_insert(0) += 1;
    }
    frek
}

fn main() {
    let frek = hitung_kata("data masuk data keluar data hilang masuk");
    assert_eq!(frek["data"], 3);
    assert_eq!(frek.get("masuk"), Some(&2));
    assert_eq!(frek.get("tidak-ada"), None);
    // urutan iterasi HashMap tidak dijamin: urutkan dulu bila perlu
    let mut kunci: Vec<&String> = frek.keys().collect();
    kunci.sort();
    assert_eq!(kunci, vec!["data", "hilang", "keluar", "masuk"]);
    println!("hashmap_demo: {} kata unik, semua uji lolos", frek.len());
}
