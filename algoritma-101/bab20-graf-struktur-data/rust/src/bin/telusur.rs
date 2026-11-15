// BFS dan DFS dasar pada Vec<Vec<usize>> (Algoritma 20.1-20.2, Kode 20.5).
// Vertex A..G dipetakan ke indeks 0..6.
use std::collections::VecDeque;

fn bangun(n: usize, edge: &[(usize, usize)]) -> Vec<Vec<usize>> {
    let mut adj = vec![Vec::new(); n];
    for &(u, v) in edge {
        adj[u].push(v);
        adj[v].push(u);
    }
    for t in adj.iter_mut() {
        t.sort();
    }
    adj
}

fn bfs(adj: &[Vec<usize>], s: usize) -> Vec<usize> {
    let mut ditemukan = vec![false; adj.len()];
    let mut urutan = Vec::new();
    let mut q = VecDeque::new();
    ditemukan[s] = true;
    q.push_back(s);
    while let Some(u) = q.pop_front() {
        urutan.push(u);
        for &v in &adj[u] {
            if !ditemukan[v] {
                ditemukan[v] = true;
                q.push_back(v);
            }
        }
    }
    urutan
}

fn dfs_iteratif(adj: &[Vec<usize>], s: usize) -> Vec<usize> {
    let mut dikunjungi = vec![false; adj.len()];
    let mut urutan = Vec::new();
    let mut stack = vec![s];
    while let Some(u) = stack.pop() {
        if dikunjungi[u] {
            continue;
        }
        dikunjungi[u] = true;
        urutan.push(u);
        for &v in adj[u].iter().rev() {
            if !dikunjungi[v] {
                stack.push(v);
            }
        }
    }
    urutan
}

fn nama(urutan: &[usize]) -> String {
    urutan.iter().map(|&i| (b'A' + i as u8) as char).collect()
}

fn main() {
    let edge = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 5), (5, 6)];
    let adj = bangun(7, &edge);
    assert_eq!(nama(&bfs(&adj, 0)), "ABCDEFG");
    assert_eq!(nama(&dfs_iteratif(&adj, 0)), "ABDEFCG");
    // rantai 100 000 vertex: stack eksplisit di heap, tidak ada stack overflow
    let n: usize = 100_000;
    let rantai: Vec<Vec<usize>> = (0..n)
        .map(|i| [i.wrapping_sub(1), i + 1].into_iter().filter(|&j| j < n).collect())
        .collect();
    assert_eq!(dfs_iteratif(&rantai, 0).len(), n);
    println!("BFS {} DFS {}: semua uji lolos", nama(&bfs(&adj, 0)), nama(&dfs_iteratif(&adj, 0)));
}
