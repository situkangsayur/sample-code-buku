// Kode 11.7: state agregat yang dapat digabung. Jalankan: cargo run
#[derive(Debug, Clone, Copy)]
struct Agregat { n: u64, total: i128, min: i64, max: i64 }

impl Agregat {
    fn kosong() -> Self { Agregat { n: 0, total: 0, min: i64::MAX, max: i64::MIN } }
    fn tambah(mut self, nominal: i64) -> Self {
        self.n += 1; self.total += nominal as i128;
        self.min = self.min.min(nominal); self.max = self.max.max(nominal);
        self
    }
    // asosiatif dan komutatif: urutan penggabungan tidak memengaruhi hasil
    fn gabung(self, o: Agregat) -> Agregat {
        Agregat { n: self.n + o.n, total: self.total + o.total,
                  min: self.min.min(o.min), max: self.max.max(o.max) }
    }
    fn rata_rata(&self) -> Option<f64> {
        (self.n > 0).then(|| self.total as f64 / self.n as f64)
    }
}

fn main() {
    // tiga partisi: batch view kemarin, dua micro-batch hari ini
    let partisi: Vec<Vec<i64>> = vec![
        vec![150_000, 2_500_000, 75_000],
        vec![4_700_000, 20_000],
        vec![310_000],
    ];
    let sebagian: Vec<Agregat> = partisi.iter()
        .map(|p| p.iter().fold(Agregat::kosong(), |a, &x| a.tambah(x)))
        .collect();
    let akhir = sebagian.iter().copied().fold(Agregat::kosong(), Agregat::gabung);
    println!("{:?}", akhir);
    println!("rata-rata = {:.0}", akhir.rata_rata().unwrap());
}
