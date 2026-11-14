// Hash table dengan separate chaining (Algoritma 18.2, Kode 18.2).
// Kunci u64, h(k) = k mod m. Indeks Rust mulai 0.

struct HashTableChaining {
    slot: Vec<Vec<(u64, String)>>,
    n: usize,
}

impl HashTableChaining {
    fn new(m: usize) -> Self {
        HashTableChaining { slot: vec![Vec::new(); m], n: 0 }
    }

    fn h(&self, k: u64) -> usize {
        (k % self.slot.len() as u64) as usize
    }

    fn put(&mut self, k: u64, v: String) {
        let i = self.h(k);
        for pasangan in self.slot[i].iter_mut() {
            if pasangan.0 == k {
                pasangan.1 = v; // kunci sudah ada: ganti nilai
                return;
            }
        }
        self.slot[i].push((k, v));
        self.n += 1;
        if self.n > self.slot.len() {
            // alpha > 1: rehash ke 2m + 1
            self.rehash(2 * self.slot.len() + 1);
        }
    }

    fn get(&self, k: u64) -> Option<&String> {
        self.slot[self.h(k)].iter().find(|p| p.0 == k).map(|p| &p.1)
    }

    fn remove(&mut self, k: u64) -> bool {
        let i = self.h(k);
        if let Some(pos) = self.slot[i].iter().position(|p| p.0 == k) {
            self.slot[i].remove(pos);
            self.n -= 1;
            return true;
        }
        false
    }

    fn rehash(&mut self, m_baru: usize) {
        let lama = std::mem::replace(&mut self.slot, vec![Vec::new(); m_baru]);
        self.n = 0;
        for rantai in lama {
            for (k, v) in rantai {
                self.put(k, v);
            }
        }
    }

    fn alpha(&self) -> f64 {
        self.n as f64 / self.slot.len() as f64
    }
}

fn main() {
    let mut t = HashTableChaining::new(11);
    for k in [23u64, 15, 42, 34, 12, 57, 31, 45] {
        t.put(k, format!("data-{}", k));
    }
    let slot1: Vec<u64> = t.slot[1].iter().map(|p| p.0).collect();
    assert_eq!(slot1, vec![23, 34, 12, 45]);
    assert!((t.alpha() - 8.0 / 11.0).abs() < 1e-12);
    assert_eq!(t.get(12).map(|s| s.as_str()), Some("data-12"));
    assert!(t.get(99).is_none());
    assert!(t.remove(34));
    assert!(!t.remove(34));
    for k in 100..110u64 {
        t.put(k, k.to_string());
    }
    assert_eq!(t.slot.len(), 23);
    for k in 100..110u64 {
        assert!(t.get(k).is_some());
    }
    println!("chaining: semua uji lolos, alpha = {:.2}", t.alpha());
}
