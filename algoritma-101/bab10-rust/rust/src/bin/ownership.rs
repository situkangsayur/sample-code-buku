// Bab 10: ownership dan borrowing sekilas.
// Jalankan: cargo run --bin ownership ; uji: cargo test --bin ownership

/// Meminjam (borrow) tanpa mengambil kepemilikan: &Vec / &[i32].
fn jumlah(a: &[i32]) -> i32 {
    let mut s = 0;
    for x in a {
        s += x;
    }
    s
}

/// Peminjaman yang dapat mengubah: &mut.
fn tambah_nol(a: &mut Vec<i32>) {
    a.push(0);
}

/// Mengambil kepemilikan: Vec dipindahkan ke fungsi, lalu dikembalikan.
fn balik(mut a: Vec<i32>) -> Vec<i32> {
    a.reverse();
    a
}

fn main() {
    let v = vec![3, 1, 4];
    println!("jumlah = {}", jumlah(&v)); // v hanya dipinjam
    println!("v masih bisa dipakai: {:?}", v);

    let mut w = v.clone(); // salinan terpisah
    tambah_nol(&mut w);
    println!("w = {:?}, v = {:?}", w, v);

    let u = v; // move: v tidak sah lagi
    println!("u = {:?}", u);
    // println!("{:?}", v); // error E0382: borrow of moved value: `v`

    let r = balik(u); // kepemilikan u pindah ke balik, lalu ke r
    println!("r = {:?}", r);

    let n = 5;
    let m = n; // i32 bertipe Copy: n tetap dapat dipakai
    println!("n = {}, m = {}", n, m);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uji_ownership() {
        let v = vec![3, 1, 4];
        assert_eq!(jumlah(&v), 8);
        let mut w = v.clone();
        tambah_nol(&mut w);
        assert_eq!(w, vec![3, 1, 4, 0]);
        assert_eq!(v, vec![3, 1, 4]);
        assert_eq!(balik(v), vec![4, 1, 3]);
    }
}
