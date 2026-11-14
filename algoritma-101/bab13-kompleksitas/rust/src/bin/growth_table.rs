// Bab 13: nilai beberapa fungsi pertumbuhan untuk n = 10, 1000, 10^6.
fn main() {
    for n in [10f64, 1000.0, 1e6] {
        let lg = n.log2();
        println!(
            "n={:>8} log n={:>6.2} n log n={:>12.3e} n^2={:>10.3e} n^3={:>10.3e}",
            n, lg, n * lg, n * n, n * n * n
        );
    }
    assert!((1000f64.log2() - 9.9658).abs() < 1e-3);
    println!("semua uji lolos");
}
