// Sengaja salah: memakai Vec setelah kepemilikannya dipindahkan.
fn jumlah(a: Vec<i32>) -> i32 {
    a.iter().sum()
}

fn main() {
    let v = vec![3, 1, 4];
    let s = jumlah(v);
    println!("{} {:?}", s, v);
}
