// Sengaja salah: meminjam &mut saat masih ada pinjaman & yang dipakai.
fn main() {
    let mut v = vec![1, 2, 3];
    let pertama = &v[0];
    v.push(4);
    println!("{}", pertama);
}
