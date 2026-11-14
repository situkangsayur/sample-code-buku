// Bab 34: mengamati kapasitas Vec saat push.
// Di std Rust 1.94 (RawVec::grow_amortized) kapasitas baru =
// max(2 * kapasitas lama, kebutuhan, kapasitas minimum 4 untuk elemen 8 byte).
// Ini detail implementasi; dokumentasi Vec tidak menjaminnya.

fn catat_kapasitas(n: usize) -> Vec<(usize, usize)> {
    let mut v: Vec<u64> = Vec::new();
    let mut hasil = Vec::new();
    let mut terakhir = v.capacity(); // 0, belum ada alokasi
    for i in 0..n {
        v.push(i as u64);
        if v.capacity() != terakhir {
            terakhir = v.capacity();
            hasil.push((v.len(), terakhir));
        }
    }
    hasil
}

fn main() {
    let hasil = catat_kapasitas(100);
    for (len, cap) in &hasil {
        println!("len {:>3} -> capacity {:>3}", len, cap);
    }
    // setiap kenaikan kapasitas paling sedikit dua kali lipat
    for w in hasil.windows(2) {
        assert!(w[1].1 >= 2 * w[0].1);
    }
    let mut v: Vec<u64> = Vec::with_capacity(100);
    let awal = v.capacity();
    for i in 0..100 {
        v.push(i);
    }
    assert_eq!(v.capacity(), awal); // tidak ada realokasi
    println!("with_capacity(100): kapasitas tetap {}", awal);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn kapasitas_cukup() {
        for (len, cap) in catat_kapasitas(1000) {
            assert!(cap >= len);
        }
    }
}
