// Decrease and conquer.

fn binary_search_rec(a: &[i64], x: i64, lo: usize, hi: usize) -> Option<usize> {
    // rentang setengah terbuka [lo, hi) agar tidak ada usize negatif
    if lo >= hi {
        return None;
    }
    let mid = lo + (hi - lo) / 2;
    if a[mid] == x {
        Some(mid)
    } else if a[mid] < x {
        binary_search_rec(a, x, mid + 1, hi)
    } else {
        binary_search_rec(a, x, lo, mid)
    }
}

fn insertion_sort_rec(a: &mut [i64]) {
    let n = a.len();
    if n <= 1 {
        return;
    }
    insertion_sort_rec(&mut a[..n - 1]);
    let kunci = a[n - 1];
    let mut j = n - 1;
    while j > 0 && a[j - 1] > kunci {
        a[j] = a[j - 1];
        j -= 1;
    }
    a[j] = kunci;
}

fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn main() {
    let a = [3, 8, 15, 21, 34, 55, 70];
    assert_eq!(binary_search_rec(&a, 34, 0, a.len()), Some(4));
    assert_eq!(binary_search_rec(&a, 4, 0, a.len()), None);
    let mut b = [5, 2, 9, 1, 7];
    insertion_sort_rec(&mut b);
    assert_eq!(b, [1, 2, 5, 7, 9]);
    println!("{}", gcd(1071, 462)); // 21
    assert_eq!(gcd(1071, 462), 21);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn insertion_acak() {
        let mut x: u64 = 5;
        for n in 0..40 {
            let mut a = Vec::new();
            for _ in 0..n {
                x = x.wrapping_mul(6364136223846793005).wrapping_add(7);
                a.push((x >> 50) as i64);
            }
            let mut b = a.clone();
            b.sort();
            insertion_sort_rec(&mut a);
            assert_eq!(a, b);
        }
    }
}
