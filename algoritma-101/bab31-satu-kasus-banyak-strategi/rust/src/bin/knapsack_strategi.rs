// Satu instance knapsack 0/1, empat strategi (Bab 31, Kode 31.3 dan Algoritma 31.2).
// Setiap fungsi mengembalikan (nilai, barang terpilih bernomor 1.., banyak langkah dasar).
type Hasil = (u64, Vec<usize>, u64);

fn brute_force(it: &[(u64, u64)], cap: u64) -> Hasil {
    let n = it.len();
    let mut best: Hasil = (0, vec![], 1 << n);
    for mask in 0u64..(1 << n) {
        let pilih: Vec<usize> = (0..n).filter(|&i| mask >> i & 1 == 1).collect();
        let w: u64 = pilih.iter().map(|&i| it[i].0).sum();
        let v: u64 = pilih.iter().map(|&i| it[i].1).sum();
        if w <= cap && v > best.0 {
            best.0 = v;
            best.1 = pilih.iter().map(|i| i + 1).collect();
        }
    }
    best
}

// Greedy menurut rasio nilai/berat terbesar.
fn greedy_rasio(it: &[(u64, u64)], cap: u64) -> Hasil {
    let mut idx: Vec<usize> = (0..it.len()).collect();
    // bandingkan v_a/w_a dengan v_b/w_b tanpa pecahan: v_a*w_b dan v_b*w_a
    idx.sort_by(|&a, &b| (it[b].1 * it[a].0).cmp(&(it[a].1 * it[b].0)));
    let (mut w, mut v, mut s) = (0, 0, vec![]);
    for i in idx {
        if w + it[i].0 <= cap {
            w += it[i].0;
            v += it[i].1;
            s.push(i + 1);
        }
    }
    s.sort();
    (v, s, it.len() as u64)
}

// Branch and bound depth-first dengan batas fractional knapsack.
fn bnb(it: &[(u64, u64)], cap: u64) -> Hasil {
    let mut idx: Vec<usize> = (0..it.len()).collect();
    idx.sort_by(|&a, &b| (it[b].1 * it[a].0).cmp(&(it[a].1 * it[b].0)));
    let its: Vec<(u64, u64)> = idx.iter().map(|&k| it[k]).collect();
    fn ub(mut i: usize, w: u64, v: u64, its: &[(u64, u64)], cap: u64) -> f64 {
        let (mut u, mut sisa) = (v as f64, cap - w);
        while i < its.len() && its[i].0 <= sisa {
            sisa -= its[i].0;
            u += its[i].1 as f64;
            i += 1;
        }
        if i < its.len() {
            u += its[i].1 as f64 * sisa as f64 / its[i].0 as f64;
        }
        u
    }
    fn go(i: usize, w: u64, v: u64, ch: &mut Vec<usize>, its: &[(u64, u64)], idx: &[usize],
          cap: u64, best: &mut Hasil) {
        best.2 += 1; // satu node dikunjungi
        if v > best.0 {
            best.0 = v;
            best.1 = ch.clone();
        }
        if i == its.len() || ub(i, w, v, its, cap) <= best.0 as f64 {
            return;
        }
        if w + its[i].0 <= cap {
            ch.push(idx[i] + 1);
            go(i + 1, w + its[i].0, v + its[i].1, ch, its, idx, cap, best);
            ch.pop();
        }
        go(i + 1, w, v, ch, its, idx, cap, best);
    }
    let mut best: Hasil = (0, vec![], 0);
    go(0, 0, 0, &mut vec![], &its, &idx, cap, &mut best);
    best.1.sort();
    best
}

fn dp(it: &[(u64, u64)], cap: u64) -> Hasil {
    let (n, c) = (it.len(), cap as usize);
    let mut t = vec![vec![0u64; c + 1]; n + 1];
    for i in 1..=n {
        let (wi, vi) = (it[i - 1].0 as usize, it[i - 1].1);
        for w in 0..=c {
            t[i][w] = t[i - 1][w];
            if wi <= w && t[i - 1][w - wi] + vi > t[i][w] {
                t[i][w] = t[i - 1][w - wi] + vi;
            }
        }
    }
    let (mut s, mut w) = (vec![], c);
    for i in (1..=n).rev() {
        if t[i][w] != t[i - 1][w] {
            s.push(i);
            w -= it[i - 1].0 as usize;
        }
    }
    s.sort();
    (t[n][c], s, (n * (c + 1)) as u64)
}

fn main() {
    let items = [(5, 10), (4, 40), (6, 30), (3, 50)];
    for (nama, h) in [
        ("brute force", brute_force(&items, 10)),
        ("greedy rasio", greedy_rasio(&items, 10)),
        ("branch and bound", bnb(&items, 10)),
        ("dynamic programming", dp(&items, 10)),
    ] {
        println!("{:<20} nilai={:>3} barang={:?} langkah={}", nama, h.0, h.1, h.2);
        assert_eq!((h.0, h.1), (90, vec![2, 4]));
    }
    let var = [(5, 10), (4, 40), (7, 63), (3, 50)];
    assert_eq!(greedy_rasio(&var, 10).0, 90);
    assert_eq!(dp(&var, 10).0, 113);
    println!("varian: greedy 90, optimum 113");
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn semua_strategi_eksak_sepakat() {
        let mut x: u64 = 27;
        let mut r = |m: u64| {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (x >> 33) % m + 1
        };
        for _ in 0..300 {
            let n = r(10) as usize;
            let it: Vec<(u64, u64)> = (0..n).map(|_| (r(15), r(50))).collect();
            let cap = r(40);
            let b = brute_force(&it, cap).0;
            assert_eq!(bnb(&it, cap).0, b);
            assert_eq!(dp(&it, cap).0, b);
            assert!(greedy_rasio(&it, cap).0 <= b);
        }
    }
}
