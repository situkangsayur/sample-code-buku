// Bab 36: menghitung id blob Git; bandingkan dengan `git hash-object <file>`.
use bab35::object_id;

fn main() {
    let isi = b"hello\n";
    let id = object_id("blob", isi);
    println!("blob {:?} -> {}", String::from_utf8_lossy(isi), id);
    assert_eq!(id, "ce013625030ba8dba906f756967f9e9ca394464a");
    // satu byte berubah, id berubah total (avalanche)
    let lain = object_id("blob", b"hellp\n");
    println!("blob \"hellp\\n\" -> {}", lain);
    assert_ne!(id, lain);
}
