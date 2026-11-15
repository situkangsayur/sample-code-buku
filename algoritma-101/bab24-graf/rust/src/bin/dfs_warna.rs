// DFS tiga warna: deteksi cycle dan topological sort (Algoritma 24.3).
// 0 json, 1 http, 2 db, 3 web, 4 app
#[derive(Clone, Copy, PartialEq)]
enum Warna {
    Putih,
    Abu,
    Hitam,
}

fn kunjungi(u: usize, adj: &[Vec<usize>], w: &mut [Warna], hasil: &mut Vec<usize>) -> bool {
    // mengembalikan true bila menemukan back edge (cycle)
    w[u] = Warna::Abu;
    let mut cycle = false;
    for &v in &adj[u] {
        match w[v] {
            Warna::Abu => cycle = true,
            Warna::Putih => cycle |= kunjungi(v, adj, w, hasil),
            Warna::Hitam => {}
        }
    }
    w[u] = Warna::Hitam;
    hasil.push(u);
    cycle
}

fn topo_dfs(adj: &[Vec<usize>]) -> Option<Vec<usize>> {
    let mut w = vec![Warna::Putih; adj.len()];
    let mut hasil = Vec::new();
    let mut cycle = false;
    for v in 0..adj.len() {
        if w[v] == Warna::Putih {
            cycle |= kunjungi(v, adj, &mut w, &mut hasil);
        }
    }
    if cycle {
        None
    } else {
        hasil.reverse();
        Some(hasil)
    }
}

fn main() {
    let adj = vec![vec![1, 2], vec![3], vec![4], vec![4], vec![]];
    assert_eq!(topo_dfs(&adj), Some(vec![0, 2, 1, 3, 4]));
    let siklus = vec![vec![1], vec![2], vec![0]];
    assert_eq!(topo_dfs(&siklus), None);
    println!("dfs_warna: semua uji lolos");
}
