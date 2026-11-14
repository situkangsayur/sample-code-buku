// Bab 14: melihat kapan Vec menambah kapasitas. Strategi pertumbuhan tidak dijamin
// dokumentasi Rust; yang dijamin hanya push O(1) amortized.
fn main() {
    let mut v: Vec<u64> = Vec::new();
    let mut last = v.capacity();
    let mut changes = vec![(0usize, last)];
    for i in 0..1000u64 {
        v.push(i);
        if v.capacity() != last {
            last = v.capacity();
            changes.push((v.len(), last));
        }
    }
    println!("(len, capacity) saat kapasitas berubah: {:?}", changes);
    assert!(changes.len() < 20);
    assert!(v.capacity() >= v.len());
    println!("semua uji lolos");
}
