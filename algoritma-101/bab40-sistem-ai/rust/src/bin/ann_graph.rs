// Bab 40: greedy beam search pada graf k-NN (lapis bawah HNSW).
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashSet};

struct SplitMix64(u64);
impl SplitMix64 {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9e3779b97f4a7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        z ^ (z >> 31)
    }
    fn uniform(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

// jarak dibungkus agar bisa diurutkan di BinaryHeap (tidak ada NaN di sini)
#[derive(PartialEq, PartialOrd, Clone, Copy)]
struct F(f64);
impl Eq for F {}
impl Ord for F {
    fn cmp(&self, o: &Self) -> std::cmp::Ordering {
        self.partial_cmp(o).unwrap()
    }
}

fn dist(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b).map(|(x, y)| (x - y) * (x - y)).sum::<f64>().sqrt()
}

fn brute(points: &[Vec<f64>], q: &[f64], k: usize) -> Vec<usize> {
    let mut v: Vec<(F, usize)> = points.iter().enumerate().map(|(i, p)| (F(dist(p, q)), i)).collect();
    v.sort();
    v.iter().take(k).map(|x| x.1).collect()
}

fn build_graph(points: &[Vec<f64>], k: usize) -> Vec<Vec<usize>> {
    let mut g: Vec<Vec<usize>> = (0..points.len())
        .map(|i| brute(points, &points[i], k + 1).into_iter().filter(|&j| j != i).take(k).collect())
        .collect();
    for i in 0..points.len() {
        for j in g[i].clone() {
            if !g[j].contains(&i) {
                g[j].push(i);
            }
        }
    }
    g
}

fn search(points: &[Vec<f64>], g: &[Vec<usize>], q: &[f64], entry: usize, ef: usize, k: usize) -> (Vec<usize>, usize) {
    let d0 = F(dist(&points[entry], q));
    let mut visited = HashSet::from([entry]);
    let mut cand = BinaryHeap::from([Reverse((d0, entry))]); // min-heap
    let mut res = BinaryHeap::from([(d0, entry)]); // max-heap
    let mut evals = 1;
    while let Some(Reverse((d, c))) = cand.pop() {
        if d > res.peek().unwrap().0 {
            break;
        }
        for &nb in &g[c] {
            if !visited.insert(nb) {
                continue;
            }
            let dn = F(dist(&points[nb], q));
            evals += 1;
            if res.len() < ef || dn < res.peek().unwrap().0 {
                cand.push(Reverse((dn, nb)));
                res.push((dn, nb));
                if res.len() > ef {
                    res.pop();
                }
            }
        }
    }
    let mut out = res.into_sorted_vec();
    out.truncate(k);
    (out.iter().map(|x| x.1).collect(), evals)
}

fn main() {
    let mut rng = SplitMix64(38);
    let (n, dim, k) = (2000, 16, 10);
    let pts: Vec<Vec<f64>> = (0..n).map(|_| (0..dim).map(|_| rng.uniform()).collect()).collect();
    let g = build_graph(&pts, 8);
    let qs: Vec<Vec<f64>> = (0..50).map(|_| (0..dim).map(|_| rng.uniform()).collect()).collect();
    for &ef in &[10, 20, 50, 100] {
        let (mut hit, mut ev) = (0, 0);
        for q in &qs {
            let exact: HashSet<usize> = brute(&pts, q, k).into_iter().collect();
            let (got, e) = search(&pts, &g, q, 0, ef, k);
            hit += got.iter().filter(|i| exact.contains(i)).count();
            ev += e;
        }
        println!("ef = {:3}: recall@10 = {:.3}, jarak per query = {}", ef, hit as f64 / 500.0, ev / 50);
        if ef == 100 {
            assert!(hit as f64 / 500.0 > 0.99);
        }
    }
    println!("semua uji ann_graph lolos");
}
