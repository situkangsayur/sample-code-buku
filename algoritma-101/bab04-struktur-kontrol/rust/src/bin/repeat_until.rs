// Kode 4.6: repeat-until di Rust dengan loop dan break (Algoritma 4.5).
fn banyak_digit(mut n: u64) -> u32 {
    let mut d = 0;
    loop {
        n /= 10; // pembagian bulat untuk u64
        d += 1;
        if n == 0 {
            break d; // loop berhenti dan bernilai d
        }
    }
}

fn main() {
    assert_eq!(banyak_digit(2026), 4);
    assert_eq!(banyak_digit(0), 1);
    println!("repeat_until: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cocok_dengan_panjang_string() {
        for n in 0..5000u64 {
            assert_eq!(banyak_digit(n) as usize, n.to_string().len());
        }
    }
}
