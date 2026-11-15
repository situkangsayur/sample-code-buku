// Bab 38: irisan dua posting list terurut (two pointer), O(|a| + |b|).

fn irisan(a: &[u32], b: &[u32]) -> Vec<u32> {
    let (mut i, mut j) = (0, 0);
    let mut hasil = Vec::new();
    while i < a.len() && j < b.len() {
        if a[i] == b[j] {
            hasil.push(a[i]);
            i += 1;
            j += 1;
        } else if a[i] < b[j] {
            i += 1;
        } else {
            j += 1;
        }
    }
    hasil
}

fn main() {
    let index = [1u32, 2, 3, 4]; // posting list "index"
    let search = [0u32, 2, 3, 4]; // posting list "search"
    let hasil = irisan(&index, &search);
    println!("index AND search -> {:?}", hasil);
    assert_eq!(hasil, vec![2, 3, 4]);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sama_dengan_cara_naif() {
        let a: Vec<u32> = (0..1000).filter(|x| x % 3 == 0).collect();
        let b: Vec<u32> = (0..1000).filter(|x| x % 5 == 0).collect();
        let naif: Vec<u32> = a.iter().copied().filter(|x| b.contains(x)).collect();
        assert_eq!(irisan(&a, &b), naif);
        assert!(irisan(&a, &[]).is_empty());
    }
}
