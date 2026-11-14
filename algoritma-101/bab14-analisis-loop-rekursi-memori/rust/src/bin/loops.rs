// Bab 14: banyak iterasi loop bersarang, segitiga, dan pembagian dua.
fn triangular(n: u64) -> u64 {
    let mut steps = 0;
    for i in 1..=n {
        for _j in 1..=i {
            steps += 1;
        }
    }
    steps
}

fn halving(n: u64) -> u64 {
    let mut steps = 0;
    let mut i = n;
    while i > 1 {
        i /= 2;
        steps += 1;
    }
    steps
}

fn main() {
    println!("triangular(16) = {}, halving(16) = {}", triangular(16), halving(16)); // 136, 4
    assert_eq!(triangular(16), 136);
    assert_eq!(halving(16), 4);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn formulas() {
        for n in [1u64, 2, 7, 8, 100] {
            assert_eq!(triangular(n), n * (n + 1) / 2);
            assert_eq!(halving(n), 63 - n.leading_zeros() as u64);
        }
    }
}
