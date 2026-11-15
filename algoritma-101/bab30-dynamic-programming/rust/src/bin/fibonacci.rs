// Fibonacci dengan memoization dan tabulation (Bab 30).
use std::collections::HashMap;

fn fib_memo(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {
    if n <= 1 {
        return n;
    }
    if let Some(&v) = memo.get(&n) {
        return v;
    }
    let v = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
    memo.insert(n, v);
    v
}

fn fib_tab(n: usize) -> u64 {
    if n <= 1 {
        return n as u64;
    }
    let mut f = vec![0u64; n + 1];
    f[1] = 1;
    for i in 2..=n {
        f[i] = f[i - 1] + f[i - 2];
    }
    f[n]
}

fn main() {
    let mut memo = HashMap::new();
    println!("fib(10) = {}", fib_tab(10));
    println!("fib(90) = {}", fib_memo(90, &mut memo));
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn memo_sama_dengan_tab() {
        for n in 0..50u64 {
            let mut memo = HashMap::new();
            assert_eq!(fib_memo(n, &mut memo), fib_tab(n as usize));
        }
        assert_eq!(fib_tab(90), 2880067194370816120);
    }
}
