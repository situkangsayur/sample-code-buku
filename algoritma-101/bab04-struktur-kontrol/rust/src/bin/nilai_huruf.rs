// Algoritma 4.2 NilaiHuruf dan Algoritma 4.4 LangkahCollatz di Rust.
fn nilai_huruf(s: u32) -> char {
    if s >= 85 {
        'A'
    } else if s >= 70 {
        'B'
    } else if s >= 55 {
        'C'
    } else if s >= 40 {
        'D'
    } else {
        'E'
    }
}

fn langkah_collatz(mut n: u64) -> u32 {
    let mut langkah = 0;
    while n != 1 {
        if n % 2 == 0 {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
        langkah += 1;
    }
    langkah
}

fn main() {
    for (s, h) in [(85, 'A'), (84, 'B'), (70, 'B'), (69, 'C'), (55, 'C'), (54, 'D'), (40, 'D'), (39, 'E')] {
        assert_eq!(nilai_huruf(s), h);
    }
    assert_eq!(langkah_collatz(6), 8);
    assert_eq!(langkah_collatz(1), 0);
    println!("nilai_huruf: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn collatz_tujuh() {
        assert_eq!(langkah_collatz(7), 16);
    }
}
