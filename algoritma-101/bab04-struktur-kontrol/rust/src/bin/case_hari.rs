// Kode 4.2: pemilihan case dengan match di Rust.
fn jenis_hari(d: u32) -> &'static str {
    match d {
        1..=5 => "hari kerja",
        6 | 7 => "akhir pekan",
        _ => "tidak valid", // wajib: match di Rust harus mencakup semua nilai
    }
}

fn main() {
    println!("{}", jenis_hari(6)); // akhir pekan
    assert_eq!(jenis_hari(1), "hari kerja");
    assert_eq!(jenis_hari(7), "akhir pekan");
    assert_eq!(jenis_hari(0), "tidak valid");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn semua_hari() {
        for d in 1..=5 {
            assert_eq!(jenis_hari(d), "hari kerja");
        }
        assert_eq!(jenis_hari(6), "akhir pekan");
        assert_eq!(jenis_hari(8), "tidak valid");
    }
}
