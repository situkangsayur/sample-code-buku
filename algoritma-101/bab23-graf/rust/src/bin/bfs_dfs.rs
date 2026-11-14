// BFS dan DFS pada adjacency list Vec<Vec<usize>> (Algoritma 23.1-20.2, Kode 23.3).
// Simpul A..G dipetakan ke indeks 0..6.
use std::collections::VecDeque;

fn bangun(n: usize, sisi: &[(usize, usize)]) -> Vec<Vec<usize>> {
    let mut adj = vec![Vec::new(); n];
    for &(u, v) in sisi {
        adj[u].push(v);
        adj[v].push(u);
    }
    for t in adj.iter_mut() {
        t.sort();
    }
    adj
}

fn bfs(adj: &[Vec<usize>], s: usize) -> (Vec<usize>, Vec<Option<usize>>) {
    let mut jarak: Vec<Option<usize>> = vec![None; adj.len()];
    let mut urutan = Vec::new();
    let mut q = VecDeque::new();
    jarak[s] = Some(0);
    q.push_back(s);
    while let Some(u) = q.pop_front() {
        urutan.push(u);
        for &v in &adj[u] {
            if jarak[v].is_none() {
                jarak[v] = Some(jarak[u].unwrap() + 1);
                q.push_back(v);
            }
        }
    }
    (urutan, jarak)
}

fn dfs(adj: &[Vec<usize>], u: usize, dikunjungi: &mut Vec<bool>, urutan: &mut Vec<usize>) {
    dikunjungi[u] = true;
    urutan.push(u);
    for &v in &adj[u] {
        if !dikunjungi[v] {
            dfs(adj, v, dikunjungi, urutan);
        }
    }
}

fn nama(urutan: &[usize]) -> String {
    urutan.iter().map(|&i| (b'A' + i as u8) as char).collect()
}

fn main() {
    // A-B, A-C, B-D, B-E, C-F, E-F, F-G
    let sisi = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 5), (5, 6)];
    let adj = bangun(7, &sisi);
    let (urutan, jarak) = bfs(&adj, 0);
    assert_eq!(nama(&urutan), "ABCDEFG");
    let j: Vec<usize> = jarak.iter().map(|x| x.unwrap()).collect();
    assert_eq!(j, vec![0, 1, 1, 2, 2, 2, 3]);
    let mut dikunjungi = vec![false; 7];
    let mut ud = Vec::new();
    dfs(&adj, 0, &mut dikunjungi, &mut ud);
    assert_eq!(nama(&ud), "ABDEFCG");
    println!("BFS {} DFS {}: semua uji lolos", nama(&urutan), nama(&ud));
}
