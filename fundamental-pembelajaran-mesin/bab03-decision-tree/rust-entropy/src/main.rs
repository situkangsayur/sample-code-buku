use std::collections::HashMap;

// Entropy (bit) dari sebuah irisan label.
fn entropy(label: &[&str]) -> f64 {
    let mut hitung: HashMap<&str, usize> = HashMap::new();
    for l in label {
        *hitung.entry(*l).or_insert(0) += 1;
    }
    let n = label.len() as f64;
    hitung.values()
        .map(|&c| { let p = c as f64 / n; -p * p.log2() })
        .sum()
}

// Information gain atribut `nilai` terhadap `label`.
fn gain(nilai: &[&str], label: &[&str]) -> f64 {
    let mut kelompok: HashMap<&str, Vec<&str>> = HashMap::new();
    for (v, l) in nilai.iter().zip(label) {
        kelompok.entry(*v).or_default().push(*l);
    }
    let n = label.len() as f64;
    let sisa: f64 = kelompok.values()
        .map(|s| s.len() as f64 / n * entropy(s))
        .sum();
    entropy(label) - sisa
}

fn main() {
    let wind = ["Weak", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong",
                "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Strong"];
    let play = ["No", "No", "Yes", "Yes", "Yes", "No", "Yes",
                "No", "Yes", "Yes", "Yes", "Yes", "Yes", "No"];
    println!("H(S)       = {:.3}", entropy(&play));      // 0.940
    println!("Gain(Wind) = {:.3}", gain(&wind, &play));  // 0.048
}
