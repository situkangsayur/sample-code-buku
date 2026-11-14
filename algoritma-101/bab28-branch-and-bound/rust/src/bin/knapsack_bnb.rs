// Knapsack 0/1 dengan branch and bound best-first (Bab 28, Kode 28.2: fungsi bound).
// Instance bersama: W = 10, barang (berat, nilai) 1=(5,10) 2=(4,40) 3=(6,30) 4=(3,50).
use std::cmp::Ordering;
use std::collections::BinaryHeap;

struct Node {
    ub: f64,
    level: usize,
    w: u64,
    v: u64,
    chosen: Vec<usize>,
}
impl PartialEq for Node {
    fn eq(&self, o: &Self) -> bool {
        self.ub.total_cmp(&o.ub) == Ordering::Equal
    }
}
impl Eq for Node {}
impl PartialOrd for Node {
    fn partial_cmp(&self, o: &Self) -> Option<Ordering> {
        Some(self.cmp(o))
    }
}
impl Ord for Node {
    // BinaryHeap Rust adalah max-heap: node dengan batas terbesar keluar lebih dulu
    fn cmp(&self, o: &Self) -> Ordering {
        self.ub.total_cmp(&o.ub)
    }
}

// Batas atas fractional knapsack mulai barang ke-i (barang sudah terurut menurut rasio).
fn bound(mut i: usize, w: u64, v: u64, its: &[(u64, u64)], cap: u64) -> f64 {
    let mut ub = v as f64;
    let mut sisa = cap - w;
    while i < its.len() && its[i].0 <= sisa {
        sisa -= its[i].0;
        ub += its[i].1 as f64;
        i += 1;
    }
    if i < its.len() {
        ub += its[i].1 as f64 * sisa as f64 / its[i].0 as f64;
    }
    ub
}

pub fn knapsack_bnb(items: &[(u64, u64)], cap: u64) -> (u64, Vec<usize>, usize) {
    let mut order: Vec<usize> = (0..items.len()).collect();
    order.sort_by(|&a, &b| {
        let ra = items[a].1 as f64 / items[a].0 as f64;
        let rb = items[b].1 as f64 / items[b].0 as f64;
        rb.total_cmp(&ra)
    });
    let its: Vec<(u64, u64)> = order.iter().map(|&k| items[k]).collect();
    let (mut best_v, mut best_s, mut made) = (0u64, Vec::new(), 1usize);
    let mut heap = BinaryHeap::new();
    heap.push(Node { ub: bound(0, 0, 0, &its, cap), level: 0, w: 0, v: 0, chosen: vec![] });
    while let Some(nd) = heap.pop() {
        if nd.ub <= best_v as f64 || nd.level == its.len() {
            continue; // dipangkas
        }
        let (wi, vi) = its[nd.level];
        for take in [true, false] {
            let (nw, nv) = if take { (nd.w + wi, nd.v + vi) } else { (nd.w, nd.v) };
            if nw > cap {
                continue; // tidak layak
            }
            let mut ch = nd.chosen.clone();
            if take {
                ch.push(order[nd.level] + 1); // nomor barang asli, mulai 1
            }
            made += 1;
            if nv > best_v {
                best_v = nv;
                best_s = ch.clone();
            }
            let ub = bound(nd.level + 1, nw, nv, &its, cap);
            if ub > best_v as f64 {
                heap.push(Node { ub, level: nd.level + 1, w: nw, v: nv, chosen: ch });
            }
        }
    }
    best_s.sort();
    (best_v, best_s, made)
}

#[cfg(test)]
fn brute(items: &[(u64, u64)], cap: u64) -> u64 {
    let n = items.len();
    (0u32..1 << n)
        .filter_map(|m| {
            let (w, v) = (0..n).filter(|i| m >> i & 1 == 1).fold((0, 0), |(w, v), i| (w + items[i].0, v + items[i].1));
            if w <= cap { Some(v) } else { None }
        })
        .max()
        .unwrap()
}

fn main() {
    let items = [(5, 10), (4, 40), (6, 30), (3, 50)];
    let (v, s, made) = knapsack_bnb(&items, 10);
    println!("nilai terbaik: {} barang: {:?} node dibuat: {}", v, s, made);
    assert_eq!((v, s, made), (90, vec![2, 4], 7));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cocok_dengan_brute_force() {
        // pembangkit acak sederhana (LCG) agar tanpa crate tambahan
        let mut x: u64 = 25;
        let mut r = |m: u64| {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            (x >> 33) % m + 1
        };
        for _ in 0..300 {
            let n = r(9) as usize;
            let items: Vec<(u64, u64)> = (0..n).map(|_| (r(12), r(40))).collect();
            let cap = r(30);
            assert_eq!(knapsack_bnb(&items, cap).0, brute(&items, cap));
        }
    }
}
