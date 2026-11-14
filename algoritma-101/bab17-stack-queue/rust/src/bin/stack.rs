// Bab 17: Vec sebagai stack dan pemeriksaan kurung.
fn balanced(text: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();
    for ch in text.chars() {
        match ch {
            '(' | '[' | '{' => stack.push(ch),
            ')' | ']' | '}' => {
                let want = match ch {
                    ')' => '(',
                    ']' => '[',
                    _ => '{',
                };
                if stack.pop() != Some(want) {
                    return false; // stack kosong (None) atau pasangan salah
                }
            }
            _ => {}
        }
    }
    stack.is_empty()
}

fn main() {
    let mut s = vec![1, 2, 3];
    s.push(4);
    assert_eq!(s.pop(), Some(4));
    assert_eq!(s.last(), Some(&3)); // peek
    println!("([)] seimbang? {}", balanced("([)]")); // false
    assert!(balanced("a[i] = f(b{c})"));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cases() {
        assert!(balanced("([]{})"));
        assert!(!balanced("([)]"));
        assert!(!balanced("(("));
        assert!(balanced(""));
        assert!(!balanced("}"));
    }
}
