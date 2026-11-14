// Merge sort. Indeks Rust mulai 0.

fn merge(left: &[i64], right: &[i64]) -> Vec<i64> {
    let mut hasil = Vec::with_capacity(left.len() + right.len());
    let (mut i, mut j) = (0, 0);
    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            hasil.push(left[i]);
            i += 1;
        } else {
            hasil.push(right[j]);
            j += 1;
        }
    }
    hasil.extend_from_slice(&left[i..]);
    hasil.extend_from_slice(&right[j..]);
    hasil
}

fn merge_sort(a: &[i64]) -> Vec<i64> {
    if a.len() <= 1 {
        return a.to_vec();
    }
    let mid = a.len() / 2;
    let left = merge_sort(&a[..mid]);
    let right = merge_sort(&a[mid..]);
    merge(&left, &right)
}

fn main() {
    let contoh = vec![38, 27, 43, 3, 9, 82, 10, 5];
    let hasil = merge_sort(&contoh);
    println!("{:?}", hasil); // [3, 5, 9, 10, 27, 38, 43, 82]
    assert_eq!(hasil, vec![3, 5, 9, 10, 27, 38, 43, 82]);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sama_dengan_sort_bawaan() {
        let mut x: u64 = 12345;
        for n in 0..60 {
            let mut a = Vec::new();
            for _ in 0..n {
                x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
                a.push((x >> 33) as i64 % 100 - 50);
            }
            let mut b = a.clone();
            b.sort();
            assert_eq!(merge_sort(&a), b);
        }
    }
}
