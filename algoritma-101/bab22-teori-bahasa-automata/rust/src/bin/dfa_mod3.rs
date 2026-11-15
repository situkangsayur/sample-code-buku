// DFA kelipatan 3 untuk bilangan biner (Algoritma 22.1, Kode 22.2).

fn delta(q: u8, b: u8) -> u8 {
    (2 * q + b) % 3
}

fn terima_mod3(w: &str) -> bool {
    let mut q: u8 = 0; // state awal q0
    for c in w.chars() {
        let b = match c {
            '0' => 0,
            '1' => 1,
            _ => return false, // simbol di luar alfabet
        };
        q = delta(q, b);
    }
    q == 0
}

fn main() {
    println!("{}", terima_mod3("1001")); // true (9)
    println!("{}", terima_mod3("1011")); // false (11)
    for n in 0u32..200 {
        assert_eq!(terima_mod3(&format!("{:b}", n)), n % 3 == 0);
    }
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn kelipatan_tiga() {
        assert!(terima_mod3("110")); // 6
        assert!(!terima_mod3("111")); // 7
        assert!(terima_mod3(""));
        assert!(!terima_mod3("12"));
    }
}
