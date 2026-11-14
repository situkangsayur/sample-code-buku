// Bab 15: array dinamis di atas blok berkapasitas tetap (Box<[Option<T>]>).
// Vec bawaan sudah melakukan ini; versi ini untuk melihat mekanismenya.
struct DynArray<T> {
    data: Box<[Option<T>]>,
    len: usize,
    copies: usize,
}

impl<T> DynArray<T> {
    fn new() -> Self {
        DynArray { data: Self::block(1), len: 0, copies: 0 }
    }

    fn block(cap: usize) -> Box<[Option<T>]> {
        (0..cap).map(|_| None).collect()
    }

    fn capacity(&self) -> usize {
        self.data.len()
    }

    fn get(&self, i: usize) -> Option<&T> {
        if i < self.len { self.data[i].as_ref() } else { None }
    }

    fn grow(&mut self) {
        let mut new_data = Self::block(2 * self.capacity());
        for k in 0..self.len {
            new_data[k] = self.data[k].take(); // pindahkan, bukan salin dalam
            self.copies += 1;
        }
        self.data = new_data;
    }

    fn push(&mut self, value: T) {
        if self.len == self.capacity() {
            self.grow();
        }
        self.data[self.len] = Some(value);
        self.len += 1;
    }

    fn insert(&mut self, i: usize, value: T) {
        assert!(i <= self.len, "indeks di luar batas");
        if self.len == self.capacity() {
            self.grow();
        }
        let mut k = self.len;
        while k > i {
            self.data[k] = self.data[k - 1].take();
            k -= 1;
        }
        self.data[i] = Some(value);
        self.len += 1;
    }

    fn remove_at(&mut self, i: usize) -> T {
        assert!(i < self.len, "indeks di luar batas");
        let value = self.data[i].take().unwrap();
        for k in i..self.len - 1 {
            self.data[k] = self.data[k + 1].take();
        }
        self.len -= 1;
        value
    }
}

fn main() {
    let mut a = DynArray::new();
    let mut caps = Vec::new();
    for v in [10, 20, 30, 40, 50] {
        a.push(v);
        caps.push(a.capacity());
    }
    println!("kapasitas setelah tiap push: {:?}", caps); // [1, 2, 4, 4, 8]
    assert_eq!(caps, vec![1, 2, 4, 4, 8]);
    assert_eq!(a.copies, 7);
    a.insert(1, 15);
    assert_eq!(a.remove_at(0), 10);
    assert_eq!(a.get(0), Some(&15));
    assert_eq!(a.get(9), None);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn amortized_copies() {
        let mut b = DynArray::new();
        for v in 0..1000 {
            b.push(v);
        }
        assert!(b.copies < 2 * 1000);
        assert_eq!(b.get(999), Some(&999));
    }
}
