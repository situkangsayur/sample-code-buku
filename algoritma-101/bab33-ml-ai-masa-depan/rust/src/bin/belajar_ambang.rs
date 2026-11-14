// Belajar ambang dari data dan batas sampel PAC (Algoritma 33.1, Kode 33.1 versi Rust).

fn belajar_ambang(data: &mut Vec<(i64, u8)>) -> (i64, usize) {
    data.sort();
    let mut calon: Vec<i64> = data.iter().map(|&(x, _)| x).collect();
    calon.push(data[data.len() - 1].0 + 1);
    let mut terbaik = (calon[0], usize::MAX);
    for &t in &calon {
        let salah = data.iter().filter(|&&(x, y)| (x >= t) != (y == 1)).count();
        if salah < terbaik.1 {
            terbaik = (t, salah);
        }
    }
    terbaik
}

fn batas_pac(ukuran_h: f64, eps: f64, delta: f64) -> u64 {
    ((ukuran_h.ln() + (1.0 / delta).ln()) / eps).ceil() as u64
}

fn main() {
    let mut data = vec![(2, 0), (3, 0), (5, 0), (6, 1), (8, 1), (9, 1), (4, 0), (7, 1)];
    let (t, salah) = belajar_ambang(&mut data);
    println!("ambang {} salah {}", t, salah); // ambang 6 salah 0
    println!("batas PAC {}", batas_pac(1001.0, 0.05, 0.01)); // 231
    assert_eq!((t, salah), (6, 0));
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn pac() {
        assert_eq!(batas_pac(1001.0, 0.05, 0.01), 231);
    }
    #[test]
    fn data_berderau() {
        let mut d = vec![(1, 0), (2, 1), (3, 0), (4, 1), (5, 1)];
        assert_eq!(belajar_ambang(&mut d).1, 1);
    }
}
