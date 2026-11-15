// ADT graf tak berarah dengan vertex bernomor 0..n-1 dan adjacency list
// Vec<Vec<usize>> (Subbab 20.4, Kode 20.3).
struct Graf {
    adj: Vec<Vec<usize>>,
}

impl Graf {
    fn baru(n: usize) -> Graf {
        Graf { adj: vec![Vec::new(); n] }
    }
    fn tambah_vertex(&mut self) -> usize {
        self.adj.push(Vec::new());
        self.adj.len() - 1 // nomor vertex baru
    }
    fn tambah_edge(&mut self, u: usize, v: usize) {
        self.adj[u].push(v);
        self.adj[v].push(u);
    }
    fn hapus_edge(&mut self, u: usize, v: usize) {
        self.adj[u].retain(|&x| x != v); // O(deg(u))
        self.adj[v].retain(|&x| x != u);
    }
    fn ada_edge(&self, u: usize, v: usize) -> bool {
        self.adj[u].contains(&v) // O(deg(u))
    }
    fn tetangga(&self, u: usize) -> &[usize] {
        &self.adj[u]
    }
    fn banyak_edge(&self) -> usize {
        self.adj.iter().map(|t| t.len()).sum::<usize>() / 2
    }
}

fn main() {
    // A..G = 0..6
    let mut g = Graf::baru(7);
    for (u, v) in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 5), (5, 6)] {
        g.tambah_edge(u, v);
    }
    assert_eq!(g.banyak_edge(), 7);
    assert_eq!(g.tetangga(1), &[0, 3, 4]);
    assert!(g.ada_edge(5, 4) && !g.ada_edge(0, 6));
    g.hapus_edge(4, 5);
    assert!(!g.ada_edge(5, 4));
    assert_eq!(g.banyak_edge(), 6);
    let h = g.tambah_vertex();
    g.tambah_edge(h, 6);
    assert_eq!(h, 7);
    assert_eq!(g.tetangga(6), &[5, 7]);
    println!("graf_adt: semua uji lolos");
}
