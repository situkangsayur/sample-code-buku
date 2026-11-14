// Bab 1: algoritma Euclid (versi sisa bagi).

fn fpb(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn main() {
    let hasil = fpb(1071, 462);
    println!("FPB(1071, 462) = {}", hasil); // 21
    assert_eq!(hasil, 21);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cocok_dengan_pengurangan() {
        for a in 1..100u64 {
            for b in 1..100u64 {
                let (mut x, mut y) = (a, b);
                while x != y {
                    if x > y { x -= y; } else { y -= x; }
                }
                assert_eq!(fpb(a, b), x);
            }
        }
    }
}
