// Sengaja salah: overflow yang terdeteksi saat kompilasi.
fn main() {
    let x: u8 = 250 + 10;
    println!("{}", x);
}
