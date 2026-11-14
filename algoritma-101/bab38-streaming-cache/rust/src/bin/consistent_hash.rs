// Bab 38: consistent hashing dengan virtual node.
use bab37_streaming_cache::h64;
use std::collections::HashMap;

struct Ring {
    points: Vec<(u64, String)>, // terurut menurut posisi
    vnodes: usize,
}

impl Ring {
    fn new(nodes: &[&str], vnodes: usize) -> Self {
        let mut r = Ring { points: Vec::new(), vnodes };
        for n in nodes {
            r.add(n);
        }
        r
    }
    fn add(&mut self, node: &str) {
        for i in 0..self.vnodes {
            self.points.push((h64(&format!("{}#{}", node, i)), node.to_string()));
        }
        self.points.sort();
    }
    // titik pertama dengan posisi > hash(key), memutar ke awal bila habis
    fn lookup(&self, key: &str) -> &str {
        let pos = h64(key);
        let i = self.points.partition_point(|(p, _)| *p <= pos);
        let i = if i == self.points.len() { 0 } else { i };
        &self.points[i].1
    }
}

fn main() {
    let keys: Vec<String> = (0..10_000).map(|i| format!("sesi:{}", i)).collect();
    let old = ["cache-A", "cache-B", "cache-C", "cache-D"];
    let new = ["cache-A", "cache-B", "cache-C", "cache-D", "cache-E"];

    let moved_mod = keys
        .iter()
        .filter(|k| old[(h64(k) % 4) as usize] != new[(h64(k) % 5) as usize])
        .count();

    let mut ring = Ring::new(&old, 100);
    let before: Vec<String> = keys.iter().map(|k| ring.lookup(k).to_string()).collect();
    ring.add("cache-E");
    let mut moved_ring = 0;
    for (k, b) in keys.iter().zip(before.iter()) {
        let a = ring.lookup(k);
        if a != b {
            assert_eq!(a, "cache-E");
            moved_ring += 1;
        }
    }
    println!("hash mod N : {} key pindah", moved_mod);
    println!("ring 100 vn: {} key pindah", moved_ring);
    assert_eq!((moved_mod, moved_ring), (7989, 1843)); // sama dengan versi Python

    let r = Ring::new(&old, 100);
    let mut load: HashMap<&str, usize> = HashMap::new();
    for k in &keys {
        *load.entry(r.lookup(k)).or_insert(0) += 1;
    }
    let mut v: Vec<usize> = load.values().cloned().collect();
    v.sort();
    println!("beban per node (100 vnode): {:?}", v);
    println!("semua uji consistent_hash lolos");
}
