// Closest pair of points.

type P = (f64, f64);

fn dist(p: P, q: P) -> f64 {
    ((p.0 - q.0).powi(2) + (p.1 - q.1).powi(2)).sqrt()
}

fn brute(pts: &[P]) -> f64 {
    let mut best = f64::INFINITY;
    for i in 0..pts.len() {
        for j in i + 1..pts.len() {
            best = best.min(dist(pts[i], pts[j]));
        }
    }
    best
}

// px terurut menurut x
fn closest_rec(px: &[P]) -> f64 {
    let n = px.len();
    if n <= 3 {
        return brute(px);
    }
    let mid = n / 2;
    let xm = px[mid].0;
    let mut d = closest_rec(&px[..mid]).min(closest_rec(&px[mid..]));
    // pita: titik yang jaraknya ke garis tengah kurang dari d, diurutkan menurut y
    let mut strip: Vec<P> = px.iter().cloned().filter(|p| (p.0 - xm).abs() < d).collect();
    strip.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
    for i in 0..strip.len() {
        let mut j = i + 1;
        while j < strip.len() && strip[j].1 - strip[i].1 < d {
            d = d.min(dist(strip[i], strip[j]));
            j += 1;
        }
    }
    d
}

fn closest_pair(points: &[P]) -> f64 {
    let mut px = points.to_vec();
    px.sort_by(|a, b| a.partial_cmp(b).unwrap());
    closest_rec(&px)
}

fn main() {
    let titik = [(2.0, 3.0), (12.0, 30.0), (40.0, 50.0), (5.0, 1.0), (12.0, 10.0), (3.0, 4.0)];
    let d = closest_pair(&titik);
    println!("{:.4}", d); // 1.4142
    assert!((d - 2f64.sqrt()).abs() < 1e-9);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sama_dengan_brute_force() {
        let mut x: u64 = 2024;
        for n in 2..80 {
            let mut pts = Vec::new();
            for _ in 0..n {
                x = x.wrapping_mul(6364136223846793005).wrapping_add(11);
                let a = ((x >> 33) % 200) as f64;
                x = x.wrapping_mul(6364136223846793005).wrapping_add(11);
                let b = ((x >> 33) % 200) as f64;
                pts.push((a, b));
            }
            assert!((closest_pair(&pts) - brute(&pts)).abs() < 1e-9);
        }
    }
}
