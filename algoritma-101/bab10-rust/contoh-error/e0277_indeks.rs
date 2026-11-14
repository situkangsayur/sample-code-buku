// Sengaja salah: indeks Vec harus usize, bukan i32.
fn main() {
    let a = vec![10, 20, 30];
    let i: i32 = 1;
    println!("{}", a[i]);
}
