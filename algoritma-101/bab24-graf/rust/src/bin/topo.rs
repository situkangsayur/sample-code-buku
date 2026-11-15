// Topological sort algoritma Kahn (Algoritma 24.2, versi Rust dari Kode 24.3).
use std::collections::VecDeque;

fn topo_kahn(n: usize, sisi: &[(usize, usize)]) -> Option<Vec<usize>> {
    let mut masuk = vec![0usize; n];
    let mut adj = vec![Vec::new(); n];
    for &(u, v) in sisi {
        adj[u].push(v);
        masuk[v] += 1;
    }
    let mut q: VecDeque<usize> = (0..n).filter(|&v| masuk[v] == 0).collect();
    let mut hasil = Vec::new();
    while let Some(u) = q.pop_front() {
        hasil.push(u);
        for &v in &adj[u] {
            masuk[v] -= 1;
            if masuk[v] == 0 {
                q.push_back(v);
            }
        }
    }
    if hasil.len() < n { None } else { Some(hasil) }
}

fn main() {
    // 0 json, 1 http, 2 db, 3 web, 4 app
    let butuh = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)];
    assert_eq!(topo_kahn(5, &butuh), Some(vec![0, 1, 2, 3, 4]));
    assert_eq!(topo_kahn(3, &[(0, 1), (1, 2), (2, 0)]), None);
    println!("topo: semua uji lolos");
}
