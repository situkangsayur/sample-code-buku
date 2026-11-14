// Hash table open addressing dengan linear probing (Algoritma 18.3, Kode 18.3).
// Slot: Kosong, Hapus (tombstone), atau Isi(kunci, nilai).

#[derive(Clone, PartialEq, Debug)]
enum Slot {
    Kosong,
    Hapus,
    Isi(u64, u64),
}

struct HashTableLinear {
    slot: Vec<Slot>,
}

impl HashTableLinear {
    fn new(m: usize) -> Self {
        HashTableLinear { slot: vec![Slot::Kosong; m] }
    }

    fn h(&self, k: u64) -> usize {
        (k % self.slot.len() as u64) as usize
    }

    // mengembalikan banyak probe; tabel dianggap tidak pernah penuh
    fn put(&mut self, k: u64, v: u64) -> usize {
        let m = self.slot.len();
        let mut i = self.h(k);
        let mut probe = 1;
        let mut bekas: Option<usize> = None;
        loop {
            match self.slot[i] {
                Slot::Kosong => break,
                Slot::Hapus => {
                    if bekas.is_none() {
                        bekas = Some(i);
                    }
                }
                Slot::Isi(kk, _) if kk == k => {
                    self.slot[i] = Slot::Isi(k, v);
                    return probe;
                }
                Slot::Isi(_, _) => {}
            }
            i = (i + 1) % m;
            probe += 1;
        }
        let tujuan = bekas.unwrap_or(i);
        self.slot[tujuan] = Slot::Isi(k, v);
        probe
    }

    fn get(&self, k: u64) -> Option<u64> {
        let m = self.slot.len();
        let mut i = self.h(k);
        for _ in 0..m {
            match self.slot[i] {
                Slot::Kosong => return None,
                Slot::Isi(kk, v) if kk == k => return Some(v),
                _ => {}
            }
            i = (i + 1) % m;
        }
        None
    }

    fn remove(&mut self, k: u64) -> bool {
        let m = self.slot.len();
        let mut i = self.h(k);
        for _ in 0..m {
            match self.slot[i] {
                Slot::Kosong => return false,
                Slot::Isi(kk, _) if kk == k => {
                    self.slot[i] = Slot::Hapus;
                    return true;
                }
                _ => {}
            }
            i = (i + 1) % m;
        }
        false
    }
}

fn main() {
    let mut t = HashTableLinear::new(11);
    let probes: Vec<usize> = [23u64, 15, 42, 34, 12, 57, 31, 45]
        .iter()
        .map(|&k| t.put(k, k))
        .collect();
    assert_eq!(probes, vec![1, 1, 1, 2, 3, 4, 2, 6]);
    assert_eq!(t.slot[6], Slot::Isi(45, 45));
    assert_eq!(t.get(45), Some(45));
    assert_eq!(t.get(1), None);
    assert!(t.remove(12));
    assert_eq!(t.slot[3], Slot::Hapus);
    assert_eq!(t.get(45), Some(45)); // tombstone tidak memutus pencarian
    t.put(56, 56);
    assert_eq!(t.slot[3], Slot::Isi(56, 56));
    println!("linear_probing: probe = {:?}, semua uji lolos", probes);
}
