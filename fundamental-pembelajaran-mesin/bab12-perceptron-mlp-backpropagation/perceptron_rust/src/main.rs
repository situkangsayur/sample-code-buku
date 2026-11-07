// Perceptron Rosenblatt dalam Rust tanpa crate tambahan. Kode 9.2 pada buku.
struct Perceptron {
    w: [f64; 2],
    b: f64,
}

impl Perceptron {
    fn prediksi(&self, x: &[f64; 2]) -> i32 {
        let z = self.w[0] * x[0] + self.w[1] * x[1] + self.b;
        if z > 0.0 { 1 } else { 0 }
    }

    // mengembalikan jumlah epoch sampai konvergen, atau None
    fn latih(&mut self, data: &[([f64; 2], i32)], eta: f64, max_epoch: usize) -> Option<usize> {
        for epoch in 1..=max_epoch {
            let mut salah = 0;
            for (x, y) in data {
                let galat = (y - self.prediksi(x)) as f64;
                if galat != 0.0 {
                    self.w[0] += eta * galat * x[0];
                    self.w[1] += eta * galat * x[1];
                    self.b += eta * galat;
                    salah += 1;
                }
            }
            if salah == 0 {
                return Some(epoch);
            }
        }
        None
    }
}

fn main() {
    let and = [([0.0, 0.0], 0), ([0.0, 1.0], 0), ([1.0, 0.0], 0), ([1.0, 1.0], 1)];
    let xor = [([0.0, 0.0], 0), ([0.0, 1.0], 1), ([1.0, 0.0], 1), ([1.0, 1.0], 0)];
    for (nama, data) in [("AND", &and), ("XOR", &xor)] {
        let mut p = Perceptron { w: [0.0; 2], b: 0.0 };
        match p.latih(data, 1.0, 20) {
            Some(e) => println!("{nama}: konvergen pada epoch {e}, w={:?}, b={}", p.w, p.b),
            None => println!("{nama}: tidak konvergen dalam 20 epoch"),
        }
    }
}
