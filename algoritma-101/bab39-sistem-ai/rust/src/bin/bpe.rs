// Bab 39: pelatihan dan encoding BPE (greedy: pasangan paling sering digabung).
use std::collections::HashMap;

type Word = Vec<String>;

fn split_word(w: &str) -> Word {
    let mut v: Word = w.chars().map(|c| c.to_string()).collect();
    v.push("_".to_string()); // penanda akhir kata
    v
}

fn merge_pair(s: &Word, a: &str, b: &str) -> Word {
    let mut out = Vec::new();
    let mut i = 0;
    while i < s.len() {
        if i + 1 < s.len() && s[i] == a && s[i + 1] == b {
            out.push(format!("{}{}", a, b));
            i += 2;
        } else {
            out.push(s[i].clone());
            i += 1;
        }
    }
    out
}

fn train(corpus: &[(&str, u32)], num_merges: usize) -> Vec<(String, String)> {
    let mut vocab: Vec<(Word, u32)> = corpus.iter().map(|(w, f)| (split_word(w), *f)).collect();
    let mut merges = Vec::new();
    for _ in 0..num_merges {
        let mut pairs: HashMap<(String, String), u32> = HashMap::new();
        for (s, f) in &vocab {
            for w in s.windows(2) {
                *pairs.entry((w[0].clone(), w[1].clone())).or_insert(0) += f;
            }
        }
        // frekuensi terbesar; seri dipecah dengan pasangan terkecil leksikografis
        let best = match pairs.iter().max_by(|x, y| x.1.cmp(y.1).then(y.0.cmp(x.0))) {
            Some((p, _)) => p.clone(),
            None => break,
        };
        vocab = vocab.iter().map(|(s, f)| (merge_pair(s, &best.0, &best.1), *f)).collect();
        merges.push(best);
    }
    merges
}

fn encode(word: &str, merges: &[(String, String)]) -> Word {
    let mut s = split_word(word);
    loop {
        // merge yang dipelajari paling awal diterapkan lebih dulu
        let mut best: Option<usize> = None;
        for w in s.windows(2) {
            if let Some(r) = merges.iter().position(|(a, b)| *a == w[0] && *b == w[1]) {
                if best.map_or(true, |x| r < x) {
                    best = Some(r);
                }
            }
        }
        match best {
            Some(r) => s = merge_pair(&s, &merges[r].0, &merges[r].1),
            None => return s,
        }
    }
}

fn main() {
    let corpus = [("makan", 6), ("makanan", 4), ("dimakan", 3), ("minum", 5), ("minuman", 3), ("tanam", 2)];
    let merges = train(&corpus, 10);
    let joined: Vec<String> = merges.iter().map(|(a, b)| format!("{}{}", a, b)).collect();
    println!("merge: {:?}", joined);
    assert_eq!(&joined[..5], &["an", "an_", "ak", "mak", "makan_"]);
    for w in ["makanan", "minuman", "tanaman"] {
        println!("encode({}) = {:?}", w, encode(w, &merges));
    }
    assert_eq!(encode("minuman", &merges), vec!["minum", "an_"]);
    assert_eq!(encode("makanan", &merges), vec!["mak", "an", "an_"]);
    let toy = train(&[("aa", 3), ("aaa", 2)], 2);
    assert_eq!(encode("aaa", &toy), vec!["aa", "a", "_"]);
    println!("semua uji bpe lolos");
}
