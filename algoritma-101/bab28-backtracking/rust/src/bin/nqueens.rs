// Bab 28: n-Queens dengan backtracking (Algoritma 28.2, Kode 28.2).
// Indeks Rust mulai 0; di buku baris dan kolom mulai 1.

fn place_ok(col: &[usize], r: usize, c: usize) -> bool {
    (0..r).all(|i| col[i] != c && col[i].abs_diff(c) != r - i)
}

fn queens(n: usize, r: usize, col: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
    if r == n {
        out.push(col.clone()); // solusi lengkap
        return;
    }
    for c in 0..n {
        if place_ok(col, r, c) {
            col[r] = c;
            queens(n, r + 1, col, out);
        }
    }
}

fn solve(n: usize) -> Vec<Vec<usize>> {
    let mut col = vec![0; n];
    let mut out = Vec::new();
    queens(n, 0, &mut col, &mut out);
    out
}

fn main() {
    let expected = [1, 0, 0, 2, 10, 4, 40, 92, 352, 724];
    for n in 1..=10 {
        let k = solve(n).len();
        assert_eq!(k, expected[n - 1]);
        println!("Q({}) = {}", n, k);
    }
    let first: Vec<usize> = solve(4)[0].iter().map(|c| c + 1).collect();
    println!("solusi pertama 4-Queens: {:?}", first); // [2, 4, 1, 3]
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn four_and_eight() {
        assert_eq!(solve(4), vec![vec![1, 3, 0, 2], vec![2, 0, 3, 1]]);
        assert_eq!(solve(8).len(), 92);
        assert_eq!(solve(3).len(), 0);
    }
}
