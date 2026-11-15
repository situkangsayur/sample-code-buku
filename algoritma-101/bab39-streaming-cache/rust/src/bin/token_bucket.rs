// Bab 39: token bucket; waktu diberikan sebagai argumen agar uji dapat diulang.
struct TokenBucket {
    capacity: f64,
    rate: f64,
    tokens: f64,
    last: f64,
}

impl TokenBucket {
    fn new(capacity: f64, rate: f64) -> Self {
        TokenBucket { capacity, rate, tokens: capacity, last: 0.0 }
    }
    fn allow(&mut self, now: f64, cost: f64) -> bool {
        let elapsed = now - self.last;
        self.tokens = (self.tokens + elapsed * self.rate).min(self.capacity);
        self.last = now;
        if self.tokens >= cost {
            self.tokens -= cost;
            true
        } else {
            false
        }
    }
}

fn main() {
    let mut tb = TokenBucket::new(3.0, 1.0);
    let times = [0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.2, 3.0, 3.0, 3.0];
    let got: Vec<bool> = times.iter().map(|&t| tb.allow(t, 1.0)).collect();
    println!("{:?}", got);
    assert_eq!(got, vec![true, true, true, false, false, true, false, true, true, false]);
    println!("semua uji token_bucket lolos");
}
