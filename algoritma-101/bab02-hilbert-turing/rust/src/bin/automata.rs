// Bab 2: DFA kelipatan tiga dan pemeriksa kurung dengan stack.

fn dfa_kelipatan_tiga(s: &str) -> bool {
    let mut r = 0u32; // state awal q0
    for b in s.chars() {
        let bit = if b == '1' { 1 } else { 0 };
        r = (2 * r + bit) % 3;
    }
    r == 0
}

fn kurung_seimbang(s: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();
    for c in s.chars() {
        match c {
            '(' => stack.push(c),
            ')' => {
                if stack.pop().is_none() {
                    return false;
                }
            }
            _ => {}
        }
    }
    stack.is_empty()
}

fn main() {
    assert!(dfa_kelipatan_tiga("1100")); // 12
    assert!(!dfa_kelipatan_tiga("111")); // 7
    assert!(kurung_seimbang("(()())"));
    assert!(!kurung_seimbang("())("));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn dfa_cocok_dengan_modulo() {
        for n in 0u32..500 {
            assert_eq!(dfa_kelipatan_tiga(&format!("{:b}", n)), n % 3 == 0);
        }
    }
}
