// Assignment problem dengan branch and bound best-first (Bab 28, Subbab 25.2).
use std::cmp::Reverse;
use std::collections::BinaryHeap;

// Biaya pasti + minimum tiap baris berikutnya pada kolom yang masih bebas.
fn lower_bound(cost: u64, assigned: &[usize], c: &[Vec<u64>]) -> u64 {
    let n = c.len();
    let mut lb = cost;
    for r in assigned.len()..n {
        lb += (0..n).filter(|j| !assigned.contains(j)).map(|j| c[r][j]).min().unwrap();
    }
    lb
}

pub fn assignment_bnb(c: &[Vec<u64>]) -> (u64, Vec<usize>) {
    let n = c.len();
    let (mut best_cost, mut best) = (u64::MAX, Vec::new());
    // Reverse membuat max-heap menjadi min-heap: batas bawah terkecil keluar lebih dulu
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((lower_bound(0, &[], c), 0u64, Vec::<usize>::new())));
    while let Some(Reverse((lb, cost, a))) = heap.pop() {
        if lb >= best_cost {
            continue;
        }
        if a.len() == n {
            best_cost = cost;
            best = a;
            continue;
        }
        let r = a.len();
        for j in 0..n {
            if a.contains(&j) {
                continue;
            }
            let nc = cost + c[r][j];
            let mut na = a.clone();
            na.push(j);
            let nlb = lower_bound(nc, &na, c);
            if nlb < best_cost {
                heap.push(Reverse((nlb, nc, na)));
            }
        }
    }
    (best_cost, best)
}

fn main() {
    let c = vec![vec![9, 2, 7, 8], vec![6, 4, 3, 7], vec![5, 8, 1, 8], vec![7, 6, 9, 4]];
    assert_eq!(lower_bound(0, &[], &c), 10);
    let (cost, a) = assignment_bnb(&c);
    let tampil: Vec<(char, usize)> = a.iter().enumerate().map(|(r, &j)| ((b'a' + r as u8) as char, j + 1)).collect();
    println!("biaya minimum: {} penugasan: {:?}", cost, tampil);
    assert_eq!((cost, a), (13, vec![1, 0, 2, 3]));
    println!("semua uji lolos");
}
