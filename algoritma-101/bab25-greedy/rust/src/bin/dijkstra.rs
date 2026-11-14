// Dijkstra dengan BinaryHeap (min-heap lewat Reverse) (Algoritma 25.5, Kode 25.4).
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn dijkstra(adj: &[Vec<(usize, u64)>], s: usize) -> Vec<u64> {
    let mut jarak = vec![u64::MAX; adj.len()];
    let mut heap = BinaryHeap::new();
    jarak[s] = 0;
    heap.push(Reverse((0u64, s)));
    while let Some(Reverse((d, u))) = heap.pop() {
        if d > jarak[u] {
            continue; // entri basi
        }
        for &(v, w) in &adj[u] {
            if d + w < jarak[v] {
                jarak[v] = d + w; // relaksasi
                heap.push(Reverse((jarak[v], v)));
            }
        }
    }
    jarak
}

fn main() {
    // A..F = 0..5
    let sisi = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8),
                (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)];
    let mut adj = vec![Vec::new(); 6];
    for &(u, v, w) in &sisi {
        adj[u].push((v, w));
        adj[v].push((u, w));
    }
    assert_eq!(dijkstra(&adj, 0), vec![0, 3, 2, 8, 10, 13]);
    println!("dijkstra: semua uji lolos");
}
