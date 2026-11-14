// Bab 37: inverted index + skor BM25 (bentuk Lucene, k1 = 1,2, b = 0,75).
use std::collections::HashMap;

const STOPWORD: [&str; 10] = ["dan", "di", "ke", "dari", "yang", "untuk", "pada", "dengan", "adalah", "the"];

fn analyzer(teks: &str) -> Vec<String> {
    teks.to_lowercase()
        .split(|c: char| !c.is_ascii_alphanumeric())
        .filter(|t| !t.is_empty() && !STOPWORD.contains(t))
        .map(String::from)
        .collect()
}

struct Index {
    posting: HashMap<String, Vec<(usize, u32)>>, // term -> (doc_id, frekuensi)
    panjang: Vec<usize>,
    avgdl: f64,
}

fn bangun(dokumen: &[&str]) -> Index {
    let mut posting: HashMap<String, Vec<(usize, u32)>> = HashMap::new();
    let mut panjang = Vec::new();
    for (d, teks) in dokumen.iter().enumerate() {
        let token = analyzer(teks);
        panjang.push(token.len());
        for t in token {
            let p = posting.entry(t).or_default();
            match p.last_mut() {
                Some((doc, f)) if *doc == d => *f += 1,
                _ => p.push((d, 1)),
            }
        }
    }
    let avgdl = panjang.iter().sum::<usize>() as f64 / panjang.len() as f64;
    Index { posting, panjang, avgdl }
}

fn cari(ix: &Index, query: &str, k1: f64, b: f64) -> Vec<(usize, f64)> {
    let n = ix.panjang.len() as f64;
    let mut skor: HashMap<usize, f64> = HashMap::new();
    for t in analyzer(query) {
        if let Some(p) = ix.posting.get(&t) {
            let nt = p.len() as f64;
            let idf = (1.0 + (n - nt + 0.5) / (nt + 0.5)).ln();
            for &(d, f) in p {
                let f = f as f64;
                let norm = k1 * (1.0 - b + b * ix.panjang[d] as f64 / ix.avgdl);
                *skor.entry(d).or_insert(0.0) += idf * f / (f + norm);
            }
        }
    }
    let mut hasil: Vec<(usize, f64)> = skor.into_iter().collect();
    hasil.sort_by(|x, y| y.1.total_cmp(&x.1).then(x.0.cmp(&y.0)));
    hasil
}

fn main() {
    let dokumen = [
        "Binary search pada array terurut",
        "B-tree adalah index di database",
        "Inverted index dipakai search engine",
        "Search engine memakai inverted index dan BM25",
        "Index database dan search engine berbeda",
    ];
    let ix = bangun(&dokumen);
    assert_eq!(ix.panjang, vec![4, 4, 5, 6, 5]);
    let hasil = cari(&ix, "inverted index bm25", 1.2, 0.75);
    for (d, s) in hasil.iter().take(3) {
        println!("doc {} skor {:.4}", d, s);
    }
    assert_eq!(hasil[0].0, 3);
    assert!((hasil[0].1 - 1.0513).abs() < 1e-4); // sama dengan bm25.py
    assert_eq!(hasil[1].0, 2);
}
