// Pengenal a^n b^n dengan stack (Algoritma 21.2).

fn terima_anbn(w: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();
    let mut fase_b = false;
    for c in w.chars() {
        match c {
            'a' => {
                if fase_b {
                    return false;
                }
                stack.push('A');
            }
            'b' => {
                fase_b = true;
                if stack.pop().is_none() {
                    return false;
                }
            }
            _ => return false,
        }
    }
    stack.is_empty()
}

fn main() {
    println!("{}", terima_anbn("aaabbb")); // true
    println!("{}", terima_anbn("abab")); // false
    for n in 0..30 {
        let a = "a".repeat(n);
        let b = "b".repeat(n);
        assert!(terima_anbn(&format!("{}{}", a, b)));
        assert!(!terima_anbn(&format!("{}a{}", a, b)));
    }
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contoh() {
        assert!(terima_anbn("ab"));
        assert!(!terima_anbn("ba"));
        assert!(!terima_anbn("aabbb"));
    }
}
