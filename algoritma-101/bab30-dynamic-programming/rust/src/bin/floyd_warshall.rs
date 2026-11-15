// Floyd-Warshall (Bab 30). None berarti tidak ada sisi.

fn floyd_warshall(w: &[Vec<Option<i64>>]) -> Vec<Vec<Option<i64>>> {
    let n = w.len();
    let mut d = w.to_vec();
    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                if let (Some(a), Some(b)) = (d[i][k], d[k][j]) {
                    if d[i][j].map_or(true, |c| a + b < c) {
                        d[i][j] = Some(a + b);
                    }
                }
            }
        }
    }
    d
}

fn graf_buku() -> Vec<Vec<Option<i64>>> {
    // simpul 1..4 di buku = indeks 0..3 di sini
    vec![
        vec![Some(0), Some(3), None, Some(7)],
        vec![Some(8), Some(0), Some(2), None],
        vec![Some(5), None, Some(0), Some(1)],
        vec![Some(2), None, None, Some(0)],
    ]
}

fn main() {
    for baris in floyd_warshall(&graf_buku()) {
        println!("{:?}", baris);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn graf_contoh() {
        let d = floyd_warshall(&graf_buku());
        let harap = [[0, 3, 5, 6], [5, 0, 2, 3], [3, 6, 0, 1], [2, 5, 7, 0]];
        for i in 0..4 {
            for j in 0..4 {
                assert_eq!(d[i][j], Some(harap[i][j]));
            }
        }
    }
}
