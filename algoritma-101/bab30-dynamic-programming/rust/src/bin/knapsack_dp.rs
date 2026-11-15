// Knapsack 0/1 dengan tabel DP (Bab 30).
// Instance bersama: W = 10, barang (5,10), (4,40), (6,30), (3,50).

fn knapsack_tabel(berat: &[usize], nilai: &[u64], kap: usize) -> Vec<Vec<u64>> {
    let n = berat.len();
    let mut v = vec![vec![0u64; kap + 1]; n + 1];
    for i in 1..=n {
        let (wi, vi) = (berat[i - 1], nilai[i - 1]); // Vec mulai 0
        for w in 0..=kap {
            v[i][w] = v[i - 1][w];
            if wi <= w && v[i - 1][w - wi] + vi > v[i][w] {
                v[i][w] = v[i - 1][w - wi] + vi;
            }
        }
    }
    v
}

fn telusur_balik(v: &[Vec<u64>], berat: &[usize], kap: usize) -> Vec<usize> {
    let mut ambil = Vec::new();
    let mut w = kap;
    for i in (1..=berat.len()).rev() {
        if v[i][w] != v[i - 1][w] {
            ambil.push(i);
            w -= berat[i - 1];
        }
    }
    ambil.reverse();
    ambil
}

fn main() {
    let (berat, nilai) = ([5, 4, 6, 3], [10, 40, 30, 50]);
    let v = knapsack_tabel(&berat, &nilai, 10);
    for (i, baris) in v.iter().enumerate() {
        println!("{} {:?}", i, baris);
    }
    println!("optimal {} barang {:?}", v[4][10], telusur_balik(&v, &berat, 10));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn instance_bersama() {
        let (berat, nilai) = ([5, 4, 6, 3], [10, 40, 30, 50]);
        let v = knapsack_tabel(&berat, &nilai, 10);
        assert_eq!(v[4][10], 90);
        assert_eq!(telusur_balik(&v, &berat, 10), vec![2, 4]);
        assert_eq!(v[4], vec![0, 0, 0, 50, 50, 50, 50, 90, 90, 90, 90]);
    }
}
