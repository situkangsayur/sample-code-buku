// Bab 17: VecDeque sebagai queue dan deque, serta maksimum jendela geser.
use std::collections::VecDeque;

fn sliding_max(a: &[i32], k: usize) -> Vec<i32> {
    let mut dq: VecDeque<usize> = VecDeque::new();
    let mut out = Vec::new();
    for (i, &v) in a.iter().enumerate() {
        while let Some(&last) = dq.back() {
            if a[last] <= v {
                dq.pop_back();
            } else {
                break;
            }
        }
        dq.push_back(i);
        if dq[0] + k <= i {
            dq.pop_front();
        }
        if i + 1 >= k {
            out.push(a[dq[0]]);
        }
    }
    out
}

fn main() {
    let mut q: VecDeque<&str> = VecDeque::new();
    q.push_back("A");
    q.push_back("B");
    q.push_front("Z");
    assert_eq!(q.pop_front(), Some("Z"));
    assert_eq!(q.pop_back(), Some("B"));
    let a = [1, 3, -1, -3, 5, 3, 6, 7];
    let m = sliding_max(&a, 3);
    println!("sliding max k=3: {:?}", m); // [3, 3, 5, 5, 6, 7]
    assert_eq!(m, vec![3, 3, 5, 5, 6, 7]);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn brute_force_agrees() {
        let a = [5, 1, 4, 2, 8, 0, 7, 3, 9, 6];
        for k in 1..=a.len() {
            let want: Vec<i32> = a.windows(k).map(|w| *w.iter().max().unwrap()).collect();
            assert_eq!(sliding_max(&a, k), want);
        }
    }
}
