// Regresi linier satu variabel dari nol: beta_1 = Sxy/Sxx, beta_0 = ybar - beta_1 xbar (Bab 10, Kode 10.7).
fn regresi(x: &[f64], y: &[f64]) -> (f64, f64) {
    let n = x.len() as f64;
    let (xb, yb) = (x.iter().sum::<f64>() / n, y.iter().sum::<f64>() / n);
    let sxy: f64 = x.iter().zip(y).map(|(xi, yi)| (xi - xb) * (yi - yb)).sum();
    let sxx: f64 = x.iter().map(|xi| (xi - xb).powi(2)).sum();
    let b1 = sxy / sxx;
    (yb - b1 * xb, b1)
}

fn main() {
    let x = [1.0, 2.0, 3.0, 4.0, 5.0];
    let y = [2.0, 4.0, 5.0, 4.0, 5.0];
    let (b0, b1) = regresi(&x, &y);
    let ybar = y.iter().sum::<f64>() / y.len() as f64;
    let rss: f64 = x.iter().zip(&y).map(|(xi, yi)| (yi - b0 - b1 * xi).powi(2)).sum();
    let tss: f64 = y.iter().map(|yi| (yi - ybar).powi(2)).sum();
    println!("y = {b0:.2} + {b1:.2} x   R2 = {:.2}", 1.0 - rss / tss);
}
