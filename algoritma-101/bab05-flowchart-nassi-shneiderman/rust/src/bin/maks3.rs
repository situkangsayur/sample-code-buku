// Algoritma 5.1 Maks3, dibandingkan dengan a.max(b).max(c).
fn maks3(a: i64, b: i64, c: i64) -> i64 {
    let mut m = if a >= b { a } else { b };
    if c > m {
        m = c;
    }
    m
}

fn main() {
    assert_eq!(maks3(4, 9, 7), 9);
    assert_eq!(maks3(5, 5, 5), 5);
    assert_eq!(maks3(2, 7, 11), 11);
    println!("maks3: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sama_dengan_max_bawaan() {
        for a in -2..3 {
            for b in -2..3 {
                for c in -2..3 {
                    assert_eq!(maks3(a, b, c), a.max(b).max(c));
                }
            }
        }
    }
}
