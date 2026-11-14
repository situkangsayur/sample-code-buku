// TSP dengan branch and bound depth-first (Bab 28, Kode 28.3). Lima kota A..E.
fn min_out(d: &[Vec<u64>]) -> Vec<u64> {
    let n = d.len();
    (0..n).map(|i| (0..n).filter(|&j| j != i).map(|j| d[i][j]).min().unwrap()).collect()
}

fn visit(d: &[Vec<u64>], m: &[u64], path: &mut Vec<usize>, cost: u64, best: &mut (u64, Vec<usize>)) {
    let n = d.len();
    let last = *path.last().unwrap();
    if path.len() == n {
        let total = cost + d[last][0]; // kembali ke kota awal
        if total < best.0 {
            *best = (total, path.clone());
        }
        return;
    }
    let lb = cost + m[last] + (0..n).filter(|k| !path.contains(k)).map(|k| m[k]).sum::<u64>();
    if lb >= best.0 {
        return; // dipangkas
    }
    for k in 0..n {
        if !path.contains(&k) {
            path.push(k);
            visit(d, m, path, cost + d[last][k], best);
            path.pop();
        }
    }
}

pub fn tsp_bnb(d: &[Vec<u64>]) -> (u64, Vec<usize>) {
    let m = min_out(d);
    let mut best = (u64::MAX, Vec::new());
    visit(d, &m, &mut vec![0], 0, &mut best);
    best
}

fn main() {
    let d = vec![
        vec![0, 3, 1, 5, 8],
        vec![3, 0, 6, 7, 9],
        vec![1, 6, 0, 4, 2],
        vec![5, 7, 4, 0, 3],
        vec![8, 9, 2, 3, 0],
    ];
    let (cost, tour) = tsp_bnb(&d);
    let s: String = tour.iter().map(|&k| (b'A' + k as u8) as char).collect();
    println!("panjang tur: {} tur: {}A", cost, s);
    assert_eq!(cost, 16);
    println!("semua uji lolos");
}
