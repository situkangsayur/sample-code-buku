//! Kode 13.4 - Scaled dot-product attention dari nol (tanpa crate).

type Mat = Vec<Vec<f64>>;

fn matmul(a: &Mat, b: &Mat) -> Mat {
    let (n, m, p) = (a.len(), b.len(), b[0].len());
    let mut c = vec![vec![0.0; p]; n];
    for i in 0..n { for k in 0..m { for j in 0..p {
        c[i][j] += a[i][k] * b[k][j];
    } } }
    c
}

fn transpose(a: &Mat) -> Mat {
    (0..a[0].len()).map(|j| a.iter().map(|r| r[j]).collect()).collect()
}

fn softmax_baris(s: &mut Mat) {
    for r in s.iter_mut() {
        let m = r.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        let z: f64 = r.iter().map(|v| (v - m).exp()).sum();
        for v in r.iter_mut() { *v = (*v - m).exp() / z; }
    }
}

fn attention(q: &Mat, k: &Mat, v: &Mat, kausal: bool) -> (Mat, Mat) {
    let dk = k[0].len() as f64;
    let mut s = matmul(q, &transpose(k));
    for i in 0..s.len() { for j in 0..s.len() {
        s[i][j] /= dk.sqrt();
        if kausal && j > i { s[i][j] = f64::NEG_INFINITY; }
    } }
    softmax_baris(&mut s);
    (matmul(&s, v), s)
}

fn cetak(judul: &str, m: &Mat) {
    println!("{judul}");
    for r in m {
        let teks: Vec<String> = r.iter().map(|v| format!("{v:7.3}")).collect();
        println!("  [{}]", teks.join(", "));
    }
}

fn main() {
    let x: Mat = vec![vec![1.0, 0.0], vec![0.0, 1.0], vec![1.0, 1.0]];
    let wq: Mat = vec![vec![1.0, 0.0], vec![1.0, 1.0]];
    let wk: Mat = vec![vec![1.0, 1.0], vec![0.0, 1.0]];
    let wv: Mat = vec![vec![1.0, 0.0], vec![0.0, 2.0]];
    let (q, k, v) = (matmul(&x, &wq), matmul(&x, &wk), matmul(&x, &wv));

    let (z, a) = attention(&q, &k, &v, false);
    cetak("A (tanpa mask):", &a);
    cetak("Z = AV:", &z);
    let (z, a) = attention(&q, &k, &v, true);
    cetak("A (causal mask):", &a);
    cetak("Z (causal mask):", &z);
}
