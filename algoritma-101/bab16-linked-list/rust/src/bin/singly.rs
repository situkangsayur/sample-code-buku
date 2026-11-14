// Bab 16: single linked list di Rust dengan Option<Box<Node>>.
// Pola ini mengikuti bab awal "Learning Rust With Entirely Too Many Linked Lists".
struct Node<T> {
    value: T,
    next: Option<Box<Node<T>>>,
}

pub struct List<T> {
    head: Option<Box<Node<T>>>,
    len: usize,
}

impl<T> List<T> {
    pub fn new() -> Self {
        List { head: None, len: 0 }
    }

    pub fn push_front(&mut self, value: T) {
        let old = self.head.take(); // ambil head lama, head menjadi None
        self.head = Some(Box::new(Node { value, next: old }));
        self.len += 1;
    }

    pub fn pop_front(&mut self) -> Option<T> {
        self.head.take().map(|node| {
            self.head = node.next;
            self.len -= 1;
            node.value
        })
    }

    pub fn peek(&self) -> Option<&T> {
        self.head.as_ref().map(|node| &node.value)
    }

    pub fn reverse(&mut self) {
        let mut prev: Option<Box<Node<T>>> = None;
        let mut cur = self.head.take();
        while let Some(mut node) = cur {
            cur = node.next.take();
            node.next = prev;
            prev = Some(node);
        }
        self.head = prev;
    }

    pub fn to_vec(&self) -> Vec<&T> {
        let mut out = Vec::new();
        let mut p = self.head.as_deref();
        while let Some(node) = p {
            out.push(&node.value);
            p = node.next.as_deref();
        }
        out
    }
}

// Drop iteratif: tanpa ini, list sangat panjang dapat menghabiskan call stack
// karena Box dihapus secara rekursif.
impl<T> Drop for List<T> {
    fn drop(&mut self) {
        let mut cur = self.head.take();
        while let Some(mut node) = cur {
            cur = node.next.take();
        }
    }
}

fn main() {
    let mut list = List::new();
    for v in [30, 20, 10] {
        list.push_front(v);
    }
    println!("{:?}", list.to_vec()); // [10, 20, 30]
    assert_eq!(list.to_vec(), vec![&10, &20, &30]);
    list.reverse();
    assert_eq!(list.peek(), Some(&30));
    assert_eq!(list.pop_front(), Some(30));
    assert_eq!(list.len, 2);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn empty_and_long() {
        let mut l: List<i32> = List::new();
        assert_eq!(l.pop_front(), None);
        l.reverse();
        assert_eq!(l.peek(), None);
        let mut big = List::new();
        for i in 0..1_000_000 {
            big.push_front(i);
        }
        assert_eq!(big.len, 1_000_000);
        // drop iteratif tidak membuat stack overflow
    }
}
