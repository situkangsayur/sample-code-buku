// Closest pair naif (Algoritma 24.2, versi Rust dari Kode 24.2).
fn closest_pair_naif(p: &[(i64, i64)]) -> ((i64, i64), (i64, i64), i64) {
    let mut terbaik = i64::MAX;
    let mut pas = (p[0], p[1]);
    for i in 0..p.len() - 1 {
        for j in i + 1..p.len() {
            let (dx, dy) = (p[i].0 - p[j].0, p[i].1 - p[j].1);
            let d2 = dx * dx + dy * dy;
            if d2 < terbaik {
                terbaik = d2;
                pas = (p[i], p[j]);
            }
        }
    }
    (pas.0, pas.1, terbaik)
}

fn main() {
    let p = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)];
    assert_eq!(closest_pair_naif(&p), ((2, 3), (3, 4), 2));
    println!("closest_pair: semua uji lolos");
}
