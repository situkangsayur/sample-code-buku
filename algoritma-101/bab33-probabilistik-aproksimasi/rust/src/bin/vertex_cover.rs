// 2-approximation vertex cover (Algoritma 33.2 versi Rust).

fn vc_aproksimasi(n: usize, sisi: &[(usize, usize)]) -> Vec<usize> {
    let mut di_cover = vec![false; n];
    for &(u, v) in sisi {
        if !di_cover[u] && !di_cover[v] {
            di_cover[u] = true;
            di_cover[v] = true;
        }
    }
    (0..n).filter(|&i| di_cover[i]).collect()
}

fn vc_optimal(n: usize, sisi: &[(usize, usize)]) -> u32 {
    (0u32..(1 << n))
        .filter(|&m| sisi.iter().all(|&(u, v)| (m >> u) & 1 == 1 || (m >> v) & 1 == 1))
        .map(|m| m.count_ones())
        .min()
        .unwrap()
}

fn main() {
    let sisi = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)];
    let a = vc_aproksimasi(5, &sisi);
    println!("aproksimasi {:?}, optimum {}", a, vc_optimal(5, &sisi)); // [0, 1, 2, 3], 2
    assert!(a.len() as u32 <= 2 * vc_optimal(5, &sisi));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn bintang() {
        let s: Vec<(usize, usize)> = (1..7).map(|i| (0, i)).collect();
        assert_eq!(vc_aproksimasi(7, &s), vec![0, 1]);
        assert_eq!(vc_optimal(7, &s), 1);
    }
}
