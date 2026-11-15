// Quick sort dengan partisi Lomuto.

fn partition(a: &mut [i64]) -> usize {
    let hi = a.len() - 1;
    let pivot = a[hi];
    let mut i = 0; // posisi berikutnya untuk elemen <= pivot
    for j in 0..hi {
        if a[j] <= pivot {
            a.swap(i, j);
            i += 1;
        }
    }
    a.swap(i, hi);
    i
}

fn quick_sort(a: &mut [i64]) {
    if a.len() <= 1 {
        return;
    }
    let p = partition(a);
    let (kiri, kanan) = a.split_at_mut(p);
    quick_sort(kiri);
    quick_sort(&mut kanan[1..]); // lewati pivot
}

fn main() {
    let mut a = vec![7, 2, 1, 6, 8, 5, 3, 4];
    let p = partition(&mut a);
    println!("{:?} {}", a, p); // [2, 1, 3, 4, 8, 5, 7, 6] 3
    assert_eq!(a, vec![2, 1, 3, 4, 8, 5, 7, 6]);
    assert_eq!(p, 3);
    quick_sort(&mut a);
    assert_eq!(a, vec![1, 2, 3, 4, 5, 6, 7, 8]);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn acak() {
        let mut x: u64 = 99;
        for n in 0..50 {
            let mut a = Vec::new();
            for _ in 0..n {
                x = x.wrapping_mul(6364136223846793005).wrapping_add(1);
                a.push((x >> 40) as i64 % 30);
            }
            let mut b = a.clone();
            b.sort();
            quick_sort(&mut a);
            assert_eq!(a, b);
        }
    }
}
