// Karatsuba. u128 cukup untuk hasil kali dua u64.

fn digits(mut x: u128) -> u32 {
    let mut d = 1;
    while x >= 10 {
        x /= 10;
        d += 1;
    }
    d
}

fn karatsuba(x: u128, y: u128) -> u128 {
    if x < 10 || y < 10 {
        return x * y;
    }
    let m = digits(x).max(digits(y)) / 2;
    let p = 10u128.pow(m);
    let (a, b) = (x / p, x % p);
    let (c, d) = (y / p, y % p);
    let ac = karatsuba(a, c);
    let bd = karatsuba(b, d);
    let tengah = karatsuba(a + b, c + d) - ac - bd; // ad + bc
    ac * p * p + tengah * p + bd
}

fn main() {
    let h = karatsuba(1234, 5678);
    println!("{}", h); // 7006652
    assert_eq!(h, 7006652);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cocok_dengan_perkalian_biasa() {
        let mut x: u64 = 7;
        for _ in 0..1000 {
            x = x.wrapping_mul(6364136223846793005).wrapping_add(3);
            let a = (x >> 4) as u128;
            x = x.wrapping_mul(6364136223846793005).wrapping_add(3);
            let b = (x >> 4) as u128;
            assert_eq!(karatsuba(a, b), a * b);
        }
    }
}
