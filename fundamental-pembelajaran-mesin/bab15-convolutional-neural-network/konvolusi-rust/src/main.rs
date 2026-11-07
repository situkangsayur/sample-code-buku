//! Kode 12.6 - Konvolusi dua dimensi satu kanal dari nol (tanpa crate).

// Konvolusi (cross-correlation) satu kanal dengan stride dan padding nol.
fn conv2d(x: &Vec<Vec<f32>>, k: &Vec<Vec<f32>>, s: usize, p: usize) -> Vec<Vec<f32>> {
    let (n, m, kk) = (x.len(), x[0].len(), k.len());
    let h = (n + 2 * p - kk) / s + 1;
    let w = (m + 2 * p - kk) / s + 1;
    let ambil = |i: isize, j: isize| -> f32 {
        if i < 0 || j < 0 || i >= n as isize || j >= m as isize { 0.0 }
        else { x[i as usize][j as usize] }
    };
    let mut y = vec![vec![0.0; w]; h];
    for i in 0..h {
        for j in 0..w {
            let mut acc = 0.0;
            for a in 0..kk {
                for b in 0..kk {
                    let xi = (i * s + a) as isize - p as isize;
                    let xj = (j * s + b) as isize - p as isize;
                    acc += k[a][b] * ambil(xi, xj);
                }
            }
            y[i][j] = acc;
        }
    }
    y
}

fn cetak(judul: &str, y: &Vec<Vec<f32>>) {
    println!("{judul}");
    for baris in y {
        println!("  {:?}", baris);
    }
}

fn main() {
    let x: Vec<Vec<f32>> = vec![
        vec![1.0, 2.0, 0.0, 1.0, 3.0],
        vec![0.0, 1.0, 3.0, 2.0, 1.0],
        vec![2.0, 1.0, 0.0, 1.0, 0.0],
        vec![1.0, 0.0, 2.0, 3.0, 1.0],
        vec![0.0, 2.0, 1.0, 0.0, 2.0],
    ];
    let k: Vec<Vec<f32>> = vec![vec![1.0, 0.0, -1.0]; 3];
    cetak("stride 1, padding 0 (Gambar 12.2):", &conv2d(&x, &k, 1, 0));
    cetak("stride 2, padding 1:", &conv2d(&x, &k, 2, 1));
}
