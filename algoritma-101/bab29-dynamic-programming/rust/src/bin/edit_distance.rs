// Edit distance Levenshtein (Bab 29).

fn edit_distance(x: &[u8], y: &[u8]) -> usize {
    let (m, n) = (x.len(), y.len());
    let mut d = vec![vec![0usize; n + 1]; m + 1];
    for i in 0..=m { d[i][0] = i; }
    for j in 0..=n { d[0][j] = j; }
    for i in 1..=m {
        for j in 1..=n {
            let beda = if x[i - 1] == y[j - 1] { 0 } else { 1 };
            d[i][j] = (d[i - 1][j] + 1)
                .min(d[i][j - 1] + 1)
                .min(d[i - 1][j - 1] + beda);
        }
    }
    d[m][n]
}

fn main() {
    println!("edit_distance(KUCING, KANCIL) = {}", edit_distance(b"KUCING", b"KANCIL"));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contoh() {
        assert_eq!(edit_distance(b"KUCING", b"KANCIL"), 4);
        assert_eq!(edit_distance(b"kitten", b"sitting"), 3);
        assert_eq!(edit_distance(b"RUMAH", b"RAMAH"), 1);
        assert_eq!(edit_distance(b"", b"abc"), 3);
    }
}
