// Bab 16: Josephus dengan circular linked list berbasis indeks (array next).
// next[i] menyimpan indeks orang sesudah i; cara ini menghindari Box dan
// tetap memakai gagasan pointer.
fn josephus(n: usize, k: usize) -> Vec<usize> {
    let mut next: Vec<usize> = (0..n).map(|i| (i + 1) % n).collect();
    let mut order = Vec::with_capacity(n);
    let mut p = n - 1; // pendahulu orang pertama
    for _ in 0..n {
        for _ in 0..k - 1 {
            p = next[p];
        }
        let out = next[p];
        order.push(out + 1); // nomor orang mulai 1
        next[p] = next[out];
    }
    order
}

fn main() {
    let order = josephus(7, 3);
    println!("urutan keluar n=7 k=3: {:?}", order); // [3, 6, 2, 7, 5, 1, 4]
    assert_eq!(order, vec![3, 6, 2, 7, 5, 1, 4]);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn formula() {
        for n in 1..30usize {
            for k in 1..6usize {
                let mut j = 0;
                for m in 2..=n {
                    j = (j + k) % m;
                }
                assert_eq!(*josephus(n, k).last().unwrap(), j + 1);
            }
        }
    }
}
