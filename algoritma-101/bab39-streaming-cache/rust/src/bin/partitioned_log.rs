// Bab 39: log append-only berpartisi dan consumer group.
use bab37_streaming_cache::fnv1a64;

struct Topic {
    partitions: Vec<Vec<(String, String)>>,
}

impl Topic {
    fn new(n: usize) -> Self {
        Topic { partitions: vec![Vec::new(); n] }
    }
    fn partition_for(&self, key: &str) -> usize {
        (fnv1a64(key.as_bytes()) % self.partitions.len() as u64) as usize
    }
    // menambah di ujung partisi; offset = indeks
    fn produce(&mut self, key: &str, value: &str) -> (usize, usize) {
        let p = self.partition_for(key);
        self.partitions[p].push((key.to_string(), value.to_string()));
        (p, self.partitions[p].len() - 1)
    }
}

struct ConsumerGroup {
    committed: Vec<usize>,
}

impl ConsumerGroup {
    fn new(n: usize) -> Self {
        ConsumerGroup { committed: vec![0; n] }
    }
    // membaca dari committed offset; log tidak berubah
    fn poll(&mut self, t: &Topic, parts: &[usize], max: usize) -> Vec<(usize, usize, String)> {
        let mut out = Vec::new();
        for &p in parts {
            let start = self.committed[p];
            let end = (start + max).min(t.partitions[p].len());
            for off in start..end {
                out.push((p, off, t.partitions[p][off].1.clone()));
            }
            self.committed[p] = end;
        }
        out
    }
}

fn main() {
    let mut t = Topic::new(3);
    let events = [
        ("mhs-01", "bayar SPP"), ("mhs-02", "bayar SPP"), ("mhs-01", "bayar praktikum"),
        ("mhs-03", "bayar SPP"), ("mhs-02", "refund"), ("mhs-01", "bayar wisuda"),
    ];
    let mut placed = Vec::new();
    for (k, v) in events.iter() {
        let (p, off) = t.produce(k, v);
        println!("{:7} {:16} -> partisi {}, offset {}", k, v, p, off);
        placed.push((p, off));
    }
    assert_eq!(placed, vec![(1, 0), (2, 0), (1, 1), (0, 0), (2, 1), (1, 2)]);

    let mut billing = ConsumerGroup::new(3);
    let mut audit = ConsumerGroup::new(3);
    let a = billing.poll(&t, &[0, 1], 10).len() + billing.poll(&t, &[2], 10).len();
    let b = audit.poll(&t, &[0, 1, 2], 10).len();
    assert_eq!((a, b), (6, 6));
    // poll kedua kosong karena offset sudah di-commit
    assert_eq!(billing.poll(&t, &[0, 1, 2], 10).len(), 0);
    println!("semua uji partitioned_log lolos");
}
