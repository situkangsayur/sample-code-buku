// Gradient descent untuk regresi linier satu fitur, tanpa crate tambahan.
// Kode 11.2 pada buku.
fn mse(x: &[f64], y: &[f64], b0: f64, b1: f64) -> f64 {
    let n = x.len() as f64;
    x.iter().zip(y).map(|(xi, yi)| (b0 + b1 * xi - yi).powi(2)).sum::<f64>() / n
}

fn main() {
    let x = [1.0, 2.0, 3.0, 4.0, 5.0];
    let y = [2.0, 4.0, 5.0, 4.0, 5.0];
    let n = x.len() as f64;
    let (mut b0, mut b1) = (0.0_f64, 0.0_f64);
    let eta = 0.05;

    for t in 0..2000 {
        // gradien MSE terhadap b0 dan b1
        let (mut g0, mut g1) = (0.0, 0.0);
        for (xi, yi) in x.iter().zip(&y) {
            let e = b0 + b1 * xi - yi;
            g0 += 2.0 * e / n;
            g1 += 2.0 * e * xi / n;
        }
        b0 -= eta * g0;
        b1 -= eta * g1;
        if t < 3 || (t + 1) % 500 == 0 {
            println!("iterasi {:4}: b0={:.4} b1={:.4} MSE={:.4}", t + 1, b0, b1, mse(&x, &y, b0, b1));
        }
    }
}
