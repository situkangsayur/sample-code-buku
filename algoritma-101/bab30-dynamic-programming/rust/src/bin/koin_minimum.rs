// Penukaran koin minimum dengan DP (Bab 30).

/// Kembalikan Some(banyak koin) atau None bila x tidak dapat dibentuk.
fn koin_minimum(koin: &[usize], x: usize) -> Option<usize> {
    const INF: usize = usize::MAX;
    let mut c = vec![INF; x + 1];
    c[0] = 0;
    for v in 1..=x {
        for &k in koin {
            if k <= v && c[v - k] != INF && c[v - k] + 1 < c[v] {
                c[v] = c[v - k] + 1;
            }
        }
    }
    if c[x] == INF { None } else { Some(c[x]) }
}

fn main() {
    println!("6 dengan koin {{1,3,4}}: {:?} koin", koin_minimum(&[1, 3, 4], 6));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contoh_buku() {
        let tabel: Vec<_> = (0..=6).map(|v| koin_minimum(&[1, 3, 4], v)).collect();
        let harap: Vec<_> = [0, 1, 2, 1, 1, 2, 2].iter().map(|&x| Some(x)).collect();
        assert_eq!(tabel, harap);
        assert_eq!(koin_minimum(&[2], 3), None);
        assert_eq!(koin_minimum(&[1, 5, 10, 25], 63), Some(6));
    }
}
