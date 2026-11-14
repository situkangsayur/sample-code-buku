// Bab 27: Sudoku dengan backtracking dan pemilihan sel MRV (Algoritma 27.5).
// Papan [[u8; 9]; 9], 0 = kosong. Indeks Rust mulai 0.

type Grid = [[u8; 9]; 9];

fn candidates(g: &Grid, r: usize, c: usize) -> Vec<u8> {
    let mut used = [false; 10];
    for i in 0..9 {
        used[g[r][i] as usize] = true;
        used[g[i][c] as usize] = true;
    }
    let (br, bc) = (3 * (r / 3), 3 * (c / 3));
    for i in br..br + 3 {
        for j in bc..bc + 3 {
            used[g[i][j] as usize] = true;
        }
    }
    (1..=9).filter(|&v| !used[v as usize]).collect()
}

fn solve(g: &mut Grid, tries: &mut u64) -> bool {
    // MRV: cari sel kosong dengan kandidat paling sedikit
    let mut best: Option<(usize, usize, Vec<u8>)> = None;
    for r in 0..9 {
        for c in 0..9 {
            if g[r][c] == 0 {
                let cand = candidates(g, r, c);
                if best.as_ref().map_or(true, |b| cand.len() < b.2.len()) {
                    best = Some((r, c, cand));
                }
            }
        }
    }
    let Some((r, c, cand)) = best else { return true };
    for v in cand {
        *tries += 1;
        g[r][c] = v;
        if solve(g, tries) {
            return true;
        }
        g[r][c] = 0; // undo
    }
    false
}

fn parse(rows: [&str; 9]) -> Grid {
    let mut g = [[0u8; 9]; 9];
    for (r, row) in rows.iter().enumerate() {
        for (c, ch) in row.bytes().enumerate() {
            g[r][c] = ch - b'0';
        }
    }
    g
}

const PUZZLE: [&str; 9] = ["530070000", "600195000", "098000060", "800060003", "400803001",
    "700020006", "060000280", "000419005", "000080079"];

fn main() {
    let mut g = parse(PUZZLE);
    let mut tries = 0;
    assert!(solve(&mut g, &mut tries));
    println!("baris pertama: {:?}, penempatan dicoba: {}", g[0], tries);
    assert_eq!(g[0], [5, 3, 4, 6, 7, 8, 9, 1, 2]);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn solution_is_valid() {
        let mut g = parse(PUZZLE);
        let mut t = 0;
        assert!(solve(&mut g, &mut t));
        for i in 0..9 {
            let mut row: Vec<u8> = g[i].to_vec();
            let mut col: Vec<u8> = (0..9).map(|r| g[r][i]).collect();
            row.sort();
            col.sort();
            assert_eq!(row, (1..=9).collect::<Vec<u8>>());
            assert_eq!(col, (1..=9).collect::<Vec<u8>>());
        }
    }
}
