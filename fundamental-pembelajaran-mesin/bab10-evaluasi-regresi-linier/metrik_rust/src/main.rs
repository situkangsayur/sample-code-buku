// Metrik dari matriks konfusi dan selang kepercayaan error (Bab 10, Kode 10.3).
struct Konfusi { tp: f64, fn_: f64, fp: f64, tn: f64 }

impl Konfusi {
    fn akurasi(&self) -> f64 { (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn_) }
    fn presisi(&self) -> f64 { self.tp / (self.tp + self.fp) }
    fn recall(&self) -> f64 { self.tp / (self.tp + self.fn_) }
    fn f1(&self) -> f64 {
        let (p, r) = (self.presisi(), self.recall());
        2.0 * p * r / (p + r)
    }
}

// Selang kepercayaan hampiran normal: err +/- z * sqrt(err(1-err)/n)
fn selang(r: f64, n: f64, z: f64) -> (f64, f64) {
    let err = r / n;
    let sd = (err * (1.0 - err) / n).sqrt();
    (err - z * sd, err + z * sd)
}

fn main() {
    let c = Konfusi { tp: 5.0, fn_: 5.0, fp: 10.0, tn: 9980.0 };
    println!("akurasi={:.4} presisi={:.3} recall={:.2} f1={:.3}",
             c.akurasi(), c.presisi(), c.recall(), c.f1());
    let (lo, hi) = selang(12.0, 40.0, 1.96);
    println!("CI95 untuk 12/40 = [{:.3}; {:.3}]", lo, hi);
}
