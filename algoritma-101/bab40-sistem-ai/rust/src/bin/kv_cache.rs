// Bab 40: menghitung perkalian proyeksi K dan V dengan dan tanpa KV cache.
const D: usize = 4;

fn matrix(seed: f64) -> [[f64; D]; D] {
    let mut m = [[0.0; D]; D];
    for i in 0..D {
        for j in 0..D {
            m[i][j] = (seed + (3 * i + j) as f64).sin() / 2.0;
        }
    }
    m
}

fn matvec(w: &[[f64; D]; D], x: &[f64; D], proj: &mut u64) -> [f64; D] {
    *proj += (D * D) as u64;
    let mut y = [0.0; D];
    for i in 0..D {
        for j in 0..D {
            y[i] += w[i][j] * x[j];
        }
    }
    y
}

fn embed(t: usize) -> [f64; D] {
    let mut e = [0.0; D];
    for i in 0..D {
        e[i] = ((t + i) as f64).cos();
    }
    e
}

fn attend(q: &[f64; D], keys: &[[f64; D]], values: &[[f64; D]], attn: &mut u64) -> [f64; D] {
    let scores: Vec<f64> = keys
        .iter()
        .map(|k| {
            *attn += D as u64;
            q.iter().zip(k).map(|(a, b)| a * b).sum::<f64>() / (D as f64).sqrt()
        })
        .collect();
    let mx = scores.iter().cloned().fold(f64::MIN, f64::max);
    let ex: Vec<f64> = scores.iter().map(|s| (s - mx).exp()).collect();
    let tot: f64 = ex.iter().sum();
    let mut out = [0.0; D];
    for (e, v) in ex.iter().zip(values) {
        *attn += D as u64;
        for i in 0..D {
            out[i] += e / tot * v[i];
        }
    }
    out
}

// mengembalikan (keluaran, perkalian proyeksi, perkalian attention)
fn generate(n: usize, use_cache: bool) -> (Vec<[f64; D]>, u64, u64) {
    let (wq, wk, wv) = (matrix(1.0), matrix(2.0), matrix(3.0));
    let (mut proj, mut attn, mut dummy) = (0u64, 0u64, 0u64);
    let mut xs = vec![embed(0)];
    let (mut ck, mut cv): (Vec<[f64; D]>, Vec<[f64; D]>) = (Vec::new(), Vec::new());
    let mut outs = Vec::new();
    for step in 0..n {
        let x = *xs.last().unwrap();
        let q = matvec(&wq, &x, &mut dummy);
        let y = if use_cache {
            ck.push(matvec(&wk, &x, &mut proj)); // hanya token baru
            cv.push(matvec(&wv, &x, &mut proj));
            attend(&q, &ck, &cv, &mut attn)
        } else {
            let ks: Vec<[f64; D]> = xs.iter().map(|xi| matvec(&wk, xi, &mut proj)).collect();
            let vs: Vec<[f64; D]> = xs.iter().map(|xi| matvec(&wv, xi, &mut proj)).collect();
            attend(&q, &ks, &vs, &mut attn)
        };
        outs.push(y);
        let e = embed(step + 1);
        let mut next = [0.0; D];
        for i in 0..D {
            next[i] = e[i] + y[i];
        }
        xs.push(next);
    }
    (outs, proj, attn)
}

fn main() {
    for &n in &[8usize, 64, 512] {
        let (o1, p1, a1) = generate(n, false);
        let (o2, p2, a2) = generate(n, true);
        for (y1, y2) in o1.iter().zip(&o2) {
            for i in 0..D {
                assert!((y1[i] - y2[i]).abs() < 1e-12);
            }
        }
        let n64 = n as u64;
        let d = D as u64;
        assert_eq!(p1, 2 * d * d * n64 * (n64 + 1) / 2);
        assert_eq!(p2, 2 * d * d * n64);
        assert_eq!(a1, a2);
        println!("n = {:4}: proyeksi tanpa cache = {:8}, dengan cache = {:6}", n, p1, p2);
    }
    let per_token: u64 = 2 * 5120 * 40 * 2; // OPT-13B, FP16
    assert_eq!(per_token, 819_200);
    println!("semua uji kv_cache lolos");
}
