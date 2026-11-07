// Optimizer Adam dari nol dalam Rust, meminimalkan MSE data jam belajar.
// Kode 10.3 pada buku.
struct Adam { lr: f64, b1: f64, b2: f64, eps: f64, m: Vec<f64>, v: Vec<f64>, t: i32 }

impl Adam {
    fn baru(n: usize, lr: f64) -> Self {
        Adam { lr, b1: 0.9, b2: 0.999, eps: 1e-8, m: vec![0.0; n], v: vec![0.0; n], t: 0 }
    }
    fn langkah(&mut self, theta: &mut [f64], g: &[f64]) {
        self.t += 1;
        for i in 0..theta.len() {
            self.m[i] = self.b1 * self.m[i] + (1.0 - self.b1) * g[i];
            self.v[i] = self.b2 * self.v[i] + (1.0 - self.b2) * g[i] * g[i];
            let m_hat = self.m[i] / (1.0 - self.b1.powi(self.t));
            let v_hat = self.v[i] / (1.0 - self.b2.powi(self.t));
            theta[i] -= self.lr * m_hat / (v_hat.sqrt() + self.eps);
        }
    }
}

fn main() {
    let x = [1.0, 2.0, 3.0, 4.0, 5.0];
    let y = [2.0, 4.0, 5.0, 4.0, 5.0];
    let mut theta = [0.0, 0.0];
    let mut opt = Adam::baru(2, 0.1);
    for t in 1..=2000 {
        let mut g = [0.0, 0.0];
        for (xi, yi) in x.iter().zip(&y) {
            let e = theta[0] + theta[1] * xi - yi;
            g[0] += 2.0 * e / 5.0;
            g[1] += 2.0 * e * xi / 5.0;
        }
        opt.langkah(&mut theta, &g);
        if t % 500 == 0 {
            println!("iterasi {t}: b0={:.4} b1={:.4}", theta[0], theta[1]);
        }
    }
}
