// Bab 35: B-tree (minimum degree T) dengan insert dan search.
// Satu node = satu page; search menghitung node yang dikunjungi.
// Indeks mulai 0 (Rust).

const T: usize = 2; // contoh kecil di buku; database memakai ratusan key per page

struct Node {
    keys: Vec<i64>,
    children: Vec<Node>,
}

impl Node {
    fn leaf(&self) -> bool {
        self.children.is_empty()
    }
}

/// Mengembalikan (ditemukan, banyak node dikunjungi).
fn search(mut x: &Node, k: i64) -> (bool, usize) {
    let mut kunjung = 0;
    loop {
        kunjung += 1;
        match x.keys.binary_search(&k) {
            Ok(_) => return (true, kunjung),
            Err(i) => {
                if x.leaf() {
                    return (false, kunjung);
                }
                x = &x.children[i];
            }
        }
    }
}

fn split_child(x: &mut Node, i: usize) {
    let y = &mut x.children[i];
    let z_keys = y.keys.split_off(T); // key T.. pindah ke z
    let tengah = y.keys.pop().unwrap(); // key T-1 naik ke x
    let z_children = if y.leaf() { Vec::new() } else { y.children.split_off(T) };
    x.keys.insert(i, tengah);
    x.children.insert(i + 1, Node { keys: z_keys, children: z_children });
}

fn insert_nonfull(x: &mut Node, k: i64) {
    let mut i = x.keys.partition_point(|&a| a <= k);
    if x.leaf() {
        x.keys.insert(i, k);
        return;
    }
    if x.children[i].keys.len() == 2 * T - 1 {
        split_child(x, i);
        if k > x.keys[i] {
            i += 1;
        }
    }
    insert_nonfull(&mut x.children[i], k);
}

fn insert(root: Node, k: i64) -> Node {
    let mut r = root;
    if r.keys.len() == 2 * T - 1 {
        let mut s = Node { keys: Vec::new(), children: vec![r] };
        split_child(&mut s, 0);
        r = s;
    }
    insert_nonfull(&mut r, k);
    r
}

fn main() {
    let mut root = Node { keys: Vec::new(), children: Vec::new() };
    for k in [10, 20, 5, 6, 12, 30, 7, 17] {
        root = insert(root, k);
    }
    println!("root {:?}", root.keys);
    for c in &root.children {
        println!("  anak {:?}", c.keys);
    }
    assert_eq!(root.keys, vec![10, 20]);
    assert_eq!(search(&root, 17), (true, 2));
    assert_eq!(search(&root, 8), (false, 2));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn banyak_key() {
        let mut root = Node { keys: Vec::new(), children: Vec::new() };
        let mut x: u64 = 34;
        let mut semua = Vec::new();
        for _ in 0..2000 {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(1);
            let k = (x >> 40) as i64;
            semua.push(k);
            root = insert(root, k);
        }
        for &k in &semua {
            assert!(search(&root, k).0);
        }
        assert!(!search(&root, -1).0);
    }
}
