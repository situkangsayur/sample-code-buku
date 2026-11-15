// N-ary tree dengan Vec<Node> sebagai list of children (Subbab N-ary Tree Bab 19).
// Contoh tree folder Gambar 19.2; ukuran file dalam KB adalah angka rekaan.
use std::collections::VecDeque;

struct Node {
    nama: String,
    ukuran: u32,
    anak: Vec<Node>,
}

impl Node {
    fn baru(nama: &str, ukuran: u32) -> Node {
        Node { nama: nama.to_string(), ukuran, anak: Vec::new() }
    }
    fn tambah_anak(&mut self, c: Node) -> &mut Node {
        self.anak.push(c);
        self.anak.last_mut().unwrap()
    }
}

fn preorder(u: &Node, kedalaman: usize, hasil: &mut Vec<(usize, String)>) {
    hasil.push((kedalaman, u.nama.clone()));
    for c in &u.anak {
        preorder(c, kedalaman + 1, hasil);
    }
}

fn total_ukuran(u: &Node) -> u32 {
    // postorder: jumlahkan semua child dulu
    u.ukuran + u.anak.iter().map(total_ukuran).sum::<u32>()
}

fn level_order(akar: &Node) -> Vec<String> {
    let mut hasil = Vec::new();
    let mut q: VecDeque<&Node> = VecDeque::from([akar]);
    while let Some(u) = q.pop_front() {
        hasil.push(u.nama.clone());
        q.extend(u.anak.iter());
    }
    hasil
}

fn contoh_folder() -> Node {
    let mut akar = Node::baru("/", 0);
    let home = akar.tambah_anak(Node::baru("home", 0));
    let ani = home.tambah_anak(Node::baru("ani", 0));
    ani.tambah_anak(Node::baru("a.py", 3));
    ani.tambah_anak(Node::baru("b.txt", 5));
    home.tambah_anak(Node::baru("budi", 0)).tambah_anak(Node::baru("c.pdf", 20));
    akar.tambah_anak(Node::baru("etc", 0)).tambah_anak(Node::baru("hosts", 1));
    let bin = akar.tambah_anak(Node::baru("bin", 0));
    for (n, kb) in [("ls", 10), ("cp", 12), ("mv", 8)] {
        bin.tambah_anak(Node::baru(n, kb));
    }
    akar
}

fn main() {
    let akar = contoh_folder();
    let mut pre = Vec::new();
    preorder(&akar, 0, &mut pre);
    let nama: Vec<&str> = pre.iter().map(|(_, n)| n.as_str()).collect();
    assert_eq!(nama, ["/", "home", "ani", "a.py", "b.txt", "budi", "c.pdf",
                      "etc", "hosts", "bin", "ls", "cp", "mv"]);
    assert_eq!(total_ukuran(&akar), 59);
    assert_eq!(level_order(&akar)[..4], ["/", "home", "etc", "bin"]);
    for (d, n) in &pre {
        println!("{}{}", "    ".repeat(*d), n);
    }
    println!("nary: semua uji lolos");
}
