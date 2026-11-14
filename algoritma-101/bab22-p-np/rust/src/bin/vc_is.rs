// Reduksi Independent Set ke Vertex Cover, diperiksa dengan brute force.

fn independen(sisi: &[(usize, usize)], mask: u32) -> bool {
    sisi.iter().all(|&(u, v)| !((mask >> u) & 1 == 1 && (mask >> v) & 1 == 1))
}

fn cover(sisi: &[(usize, usize)], mask: u32) -> bool {
    sisi.iter().all(|&(u, v)| (mask >> u) & 1 == 1 || (mask >> v) & 1 == 1)
}

fn ada(n: usize, k: u32, uji: &dyn Fn(u32) -> bool) -> bool {
    (0u32..(1 << n)).any(|m| m.count_ones() == k && uji(m))
}

fn main() {
    let sisi = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)];
    let n = 5;
    for k in 0..=5u32 {
        let a = ada(n, k, &|m| independen(&sisi, m));
        let b = ada(n, n as u32 - k, &|m| cover(&sisi, m));
        assert_eq!(a, b);
        println!("k = {}: independent set {} | vertex cover {}", k, a, b);
    }
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn komplemen() {
        let sisi = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)];
        let s = 0b10101; // {0, 2, 4}
        assert!(independen(&sisi, s));
        assert!(cover(&sisi, !s & 0b11111)); // {1, 3}
    }
}
