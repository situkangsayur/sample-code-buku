// Bab 13: menghitung pasangan i < j dengan a[i] + a[j] == x (versi naif O(n^2)).
// Indeks Rust mulai 0, pseudocode di buku mulai 1.

fn count_pairs_naive(a: &[i64], x: i64) -> (u64, u64) {
    let n = a.len();
    let mut count = 0u64;
    let mut steps = 0u64;
    for i in 0..n.saturating_sub(1) {
        for j in (i + 1)..n {
            steps += 1;
            if a[i] + a[j] == x {
                count += 1;
            }
        }
    }
    (count, steps)
}

fn linear_search_steps(a: &[i64], x: i64) -> usize {
    let mut steps = 0;
    for &v in a {
        steps += 1;
        if v == x {
            break;
        }
    }
    steps
}

fn main() {
    let a = [3, 1, 4, 1, 5];
    let (count, steps) = count_pairs_naive(&a, 5);
    println!("pasangan berjumlah 5: {} perbandingan: {}", count, steps); // 2 10
    assert_eq!((count, steps), (2, 10));

    let arr: Vec<i64> = (1..=10).collect();
    println!(
        "linear search n=10: best {} worst {}",
        linear_search_steps(&arr, 1),
        linear_search_steps(&arr, 99)
    );
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn steps_follow_formula() {
        for n in [0usize, 1, 2, 5, 10, 100] {
            let v: Vec<i64> = (0..n as i64).collect();
            let (_, s) = count_pairs_naive(&v, -1);
            assert_eq!(s as usize, n * n.saturating_sub(1) / 2);
        }
    }

    #[test]
    fn small_example() {
        assert_eq!(count_pairs_naive(&[3, 1, 4, 1, 5], 5).0, 2);
        assert_eq!(count_pairs_naive(&[2, 2, 2], 4).0, 3);
    }
}
