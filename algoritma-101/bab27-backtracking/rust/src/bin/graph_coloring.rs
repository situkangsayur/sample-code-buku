// Bab 27: pewarnaan graf dengan m warna (Algoritma 27.4, Kode 27.4).
// Simpul 0..n-1 (A..E di buku); warna 1..m, 0 = belum diwarnai.

fn go(adj: &[Vec<usize>], m: usize, v: usize, color: &mut Vec<usize>) -> bool {
    if v == adj.len() {
        return true;
    }
    for c in 1..=m {
        if adj[v].iter().all(|&u| color[u] != c) {
            color[v] = c;
            if go(adj, m, v + 1, color) {
                return true;
            }
            color[v] = 0; // undo
        }
    }
    false
}

fn color_graph(adj: &[Vec<usize>], m: usize) -> Option<Vec<usize>> {
    let mut color = vec![0; adj.len()];
    if go(adj, m, 0, &mut color) { Some(color) } else { None }
}

fn build(n: usize, edges: &[(usize, usize)]) -> Vec<Vec<usize>> {
    let mut adj = vec![Vec::new(); n];
    for &(u, v) in edges {
        adj[u].push(v);
        adj[v].push(u);
    }
    adj
}

const EDGES: [(usize, usize); 7] = [(0, 1), (0, 2), (1, 2), (1, 4), (2, 3), (2, 4), (3, 4)];

fn main() {
    let adj = build(5, &EDGES);
    let c = color_graph(&adj, 3).expect("3 warna cukup");
    println!("pewarnaan: {:?}", c); // [1, 2, 3, 2, 1]
    assert_eq!(c, vec![1, 2, 3, 2, 1]);
    assert!(color_graph(&adj, 2).is_none());
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn k4_needs_four() {
        let e: Vec<(usize, usize)> = (0..4).flat_map(|a| (a + 1..4).map(move |b| (a, b))).collect();
        let k4 = build(4, &e);
        assert!(color_graph(&k4, 3).is_none());
        assert!(color_graph(&k4, 4).is_some());
    }
}
