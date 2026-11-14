// Bab 27: sum of subsets dengan backtracking (Algoritma 27.3; versi Python di Kode 27.3).
// w harus terurut naik. Indeks Rust mulai 0.

fn go(w: &[u64], d: u64, i: usize, s: u64, rest: u64,
      chosen: &mut Vec<u64>, out: &mut Vec<Vec<u64>>) {
    if s == d {
        out.push(chosen.clone());
        return;
    }
    if i == w.len() || s + w[i] > d || s + rest < d {
        return; // daun atau simpul yang tidak menjanjikan
    }
    chosen.push(w[i]); // ambil w[i]
    go(w, d, i + 1, s + w[i], rest - w[i], chosen, out);
    chosen.pop();
    go(w, d, i + 1, s, rest - w[i], chosen, out); // lewati w[i]
}

fn sum_of_subsets(w: &[u64], d: u64) -> Vec<Vec<u64>> {
    let mut w = w.to_vec();
    w.sort();
    let total: u64 = w.iter().sum();
    let mut out = Vec::new();
    go(&w, d, 0, 0, total, &mut Vec::new(), &mut out);
    out
}

fn main() {
    let sols = sum_of_subsets(&[3, 5, 6, 7], 15);
    println!("{:?}", sols); // [[3, 5, 7]]
    assert_eq!(sols, vec![vec![3, 5, 7]]);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn horowitz_instance() {
        let mut sols = sum_of_subsets(&[5, 10, 12, 13, 15, 18], 30);
        sols.sort();
        assert_eq!(sols, vec![vec![5, 10, 15], vec![5, 12, 13], vec![12, 18]]);
        assert!(sum_of_subsets(&[2, 4, 6], 5).is_empty());
    }
}
