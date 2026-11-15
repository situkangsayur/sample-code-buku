// Longest common subsequence (Bab 30).

fn lcs_panjang(x: &[u8], y: &[u8]) -> usize {
    let (m, n) = (x.len(), y.len());
    let mut t = vec![vec![0usize; n + 1]; m + 1];
    for i in 1..=m {
        for j in 1..=n {
            t[i][j] = if x[i - 1] == y[j - 1] {
                t[i - 1][j - 1] + 1
            } else {
                t[i - 1][j].max(t[i][j - 1])
            };
        }
    }
    t[m][n]
}

fn main() {
    println!("LCS(BANDUNG, BANTEN) = {}", lcs_panjang(b"BANDUNG", b"BANTEN"));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contoh() {
        assert_eq!(lcs_panjang(b"BANDUNG", b"BANTEN"), 4);
        assert_eq!(lcs_panjang(b"ABCBDAB", b"BDCABA"), 4);
        assert_eq!(lcs_panjang(b"", b"ABC"), 0);
    }
}
