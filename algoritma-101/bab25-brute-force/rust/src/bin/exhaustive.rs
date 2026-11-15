// Exhaustive search: TSP, knapsack 0/1, assignment (Algoritma 25.3-21.4, Kode 25.4).
// Permutasi dibangkitkan secara rekursif dengan menukar elemen.

fn permutasi(a: &mut Vec<usize>, k: usize, f: &mut dyn FnMut(&[usize])) {
    if k == a.len() {
        f(a);
        return;
    }
    for i in k..a.len() {
        a.swap(k, i);
        permutasi(a, k + 1, f);
        a.swap(k, i);
    }
}

fn tsp_brute(d: &[[u32; 4]; 4]) -> (Vec<usize>, u32) {
    let mut sisa: Vec<usize> = (1..4).collect(); // kota 0 = A tetap di awal
    let mut terbaik = (Vec::new(), u32::MAX);
    permutasi(&mut sisa, 0, &mut |p| {
        let mut rute = vec![0];
        rute.extend_from_slice(p);
        rute.push(0);
        let panjang: u32 = rute.windows(2).map(|w| d[w[0]][w[1]]).sum();
        if panjang < terbaik.1 {
            terbaik = (rute, panjang);
        }
    });
    terbaik
}

fn knapsack_brute(berat: &[u32], nilai: &[u32], w: u32) -> (u32, u32) {
    let n = berat.len();
    let mut terbaik = (0u32, 0u32); // (mask, nilai)
    for mask in 0u32..(1 << n) {
        let (mut b, mut v) = (0, 0);
        for i in 0..n {
            if mask >> i & 1 == 1 {
                b += berat[i];
                v += nilai[i];
            }
        }
        if b <= w && v > terbaik.1 {
            terbaik = (mask, v);
        }
    }
    terbaik
}

fn assignment_brute(c: &[[u32; 4]; 4]) -> (Vec<usize>, u32) {
    let mut p: Vec<usize> = (0..4).collect();
    let mut terbaik = (Vec::new(), u32::MAX);
    permutasi(&mut p, 0, &mut |q| {
        let total: u32 = (0..4).map(|i| c[i][q[i]]).sum();
        if total < terbaik.1 {
            terbaik = (q.to_vec(), total);
        }
    });
    terbaik
}

fn main() {
    // A, B, C, D = 0, 1, 2, 3
    let d = [[0, 2, 9, 10], [2, 0, 6, 4], [9, 6, 0, 3], [10, 4, 3, 0]];
    let (rute, panjang) = tsp_brute(&d);
    assert_eq!(panjang, 18);
    assert!(rute == vec![0, 1, 3, 2, 0] || rute == vec![0, 2, 3, 1, 0]);

    let (mask, v) = knapsack_brute(&[5, 4, 6, 3], &[10, 40, 30, 50], 10);
    assert_eq!((mask, v), (0b1010, 90)); // barang 2 dan 4
    // varian barang 3 = (7, 63): optimum barang 3 dan 4, nilai 113
    assert_eq!(knapsack_brute(&[5, 4, 7, 3], &[10, 40, 63, 50], 10), (0b1100, 113));

    let c = [[8, 3, 6, 9], [5, 7, 2, 6], [4, 9, 8, 3], [7, 5, 9, 4]];
    assert_eq!(assignment_brute(&c), (vec![1, 2, 0, 3], 13));
    println!("exhaustive: TSP 18, knapsack 90, assignment 13; semua uji lolos");
}
