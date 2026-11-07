// Kode 1.2: gradient descent satu dimensi tanpa pustaka tambahan.
// L(theta) = (theta - 3)^2, turunannya 2 (theta - 3)
fn turunan(theta: f64) -> f64 {
    2.0 * (theta - 3.0)
}

fn main() {
    let eta = 0.1; // learning rate
    let mut theta = 0.0; // tebakan awal
    for t in 1..=30 {
        let g = turunan(theta);
        if g.abs() < 1e-6 {
            break; // sudah cukup datar
        }
        theta -= eta * g;
        if t <= 3 || t % 10 == 0 {
            println!("langkah {:2}: theta = {:.4}", t, theta);
        }
    }
}
