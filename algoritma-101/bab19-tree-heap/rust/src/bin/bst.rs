// Binary search tree dengan Option<Box<Node>> (Algoritma 19.1, Kode 19.2).

struct Node {
    kunci: i32,
    kiri: Option<Box<Node>>,
    kanan: Option<Box<Node>>,
}

fn sisip(akar: &mut Option<Box<Node>>, kunci: i32) {
    match akar {
        None => *akar = Some(Box::new(Node { kunci, kiri: None, kanan: None })),
        Some(node) => {
            if kunci < node.kunci {
                sisip(&mut node.kiri, kunci);
            } else if kunci > node.kunci {
                sisip(&mut node.kanan, kunci);
            } // sama: abaikan duplikat
        }
    }
}

// mengembalikan (ketemu, banyak perbandingan)
fn cari(akar: &Option<Box<Node>>, kunci: i32) -> (bool, usize) {
    let mut x = akar;
    let mut langkah = 0;
    while let Some(node) = x {
        langkah += 1;
        if kunci == node.kunci {
            return (true, langkah);
        }
        x = if kunci < node.kunci { &node.kiri } else { &node.kanan };
    }
    (false, langkah)
}

fn inorder(akar: &Option<Box<Node>>, hasil: &mut Vec<i32>) {
    if let Some(node) = akar {
        inorder(&node.kiri, hasil);
        hasil.push(node.kunci);
        inorder(&node.kanan, hasil);
    }
}

fn tinggi(akar: &Option<Box<Node>>) -> i32 {
    match akar {
        None => -1,
        Some(node) => 1 + tinggi(&node.kiri).max(tinggi(&node.kanan)),
    }
}

fn main() {
    let mut akar: Option<Box<Node>> = None;
    for k in [50, 30, 70, 20, 40, 60, 80, 35] {
        sisip(&mut akar, k);
    }
    let mut urut = Vec::new();
    inorder(&akar, &mut urut);
    assert_eq!(urut, vec![20, 30, 35, 40, 50, 60, 70, 80]);
    assert_eq!(tinggi(&akar), 3);
    assert_eq!(cari(&akar, 35), (true, 4));
    assert_eq!(cari(&akar, 65), (false, 3));

    let mut rantai: Option<Box<Node>> = None;
    for k in 1..=10 {
        sisip(&mut rantai, k);
    }
    assert_eq!(tinggi(&rantai), 9);
    println!("bst: semua uji lolos");
}
