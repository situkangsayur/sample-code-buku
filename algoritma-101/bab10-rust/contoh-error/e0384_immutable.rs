// Sengaja salah: mengubah variabel yang tidak mut.
fn main() {
    let total = 0;
    for i in 1..=3 {
        total += i;
    }
    println!("{}", total);
}
