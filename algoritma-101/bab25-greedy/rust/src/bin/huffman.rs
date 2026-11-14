// Huffman coding dengan BinaryHeap dan Reverse (Algoritma 25.4).
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

enum Pohon {
    Daun(char),
    Gabung(Box<Pohon>, Box<Pohon>),
}

fn kode(t: &Pohon, awalan: String, hasil: &mut HashMap<char, String>) {
    match t {
        Pohon::Daun(c) => {
            hasil.insert(*c, awalan);
        }
        Pohon::Gabung(a, b) => {
            kode(a, awalan.clone() + "0", hasil);
            kode(b, awalan + "1", hasil);
        }
    }
}

fn huffman(frek: &[(char, u32)]) -> HashMap<char, String> {
    let mut simpan: Vec<Option<Pohon>> = Vec::new();
    // heap berisi (frekuensi, nomor urut); nomor urut juga indeks ke simpan
    let mut heap = BinaryHeap::new();
    for &(c, f) in frek {
        heap.push(Reverse((f, simpan.len())));
        simpan.push(Some(Pohon::Daun(c)));
    }
    while heap.len() > 1 {
        let Reverse((f1, i)) = heap.pop().unwrap();
        let Reverse((f2, j)) = heap.pop().unwrap();
        let t = Pohon::Gabung(Box::new(simpan[i].take().unwrap()),
                              Box::new(simpan[j].take().unwrap()));
        heap.push(Reverse((f1 + f2, simpan.len())));
        simpan.push(Some(t));
    }
    let Reverse((_, akar)) = heap.pop().unwrap();
    let mut hasil = HashMap::new();
    kode(simpan[akar].as_ref().unwrap(), String::new(), &mut hasil);
    hasil
}

fn main() {
    let teks = "ABRAKADABRA";
    // urut abjad, sama dengan versi Python
    let frek = [('A', 5), ('B', 2), ('D', 1), ('K', 1), ('R', 2)];
    let k = huffman(&frek);
    let total: usize = teks.chars().map(|c| k[&c].len()).sum();
    assert_eq!(total, 23);
    assert_eq!(k[&'A'], "0");
    assert_eq!(k[&'D'], "100");
    println!("huffman: total {} bit, semua uji lolos", total);
}
