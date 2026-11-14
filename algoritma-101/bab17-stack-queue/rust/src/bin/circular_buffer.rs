// Bab 17: queue berkapasitas tetap dengan circular buffer.
struct CircularQueue<T> {
    buf: Vec<Option<T>>,
    head: usize,
    size: usize,
}

impl<T> CircularQueue<T> {
    fn with_capacity(cap: usize) -> Self {
        CircularQueue { buf: (0..cap).map(|_| None).collect(), head: 0, size: 0 }
    }

    fn enqueue(&mut self, x: T) -> Result<(), T> {
        let cap = self.buf.len();
        if self.size == cap {
            return Err(x); // penuh: kembalikan nilai ke pemanggil
        }
        let tail = (self.head + self.size) % cap;
        self.buf[tail] = Some(x);
        self.size += 1;
        Ok(())
    }

    fn dequeue(&mut self) -> Option<T> {
        if self.size == 0 {
            return None;
        }
        let x = self.buf[self.head].take();
        self.head = (self.head + 1) % self.buf.len();
        self.size -= 1;
        x
    }
}

fn main() {
    let mut q = CircularQueue::with_capacity(4);
    for x in ['A', 'B', 'C'] {
        q.enqueue(x).unwrap();
    }
    assert_eq!(q.dequeue(), Some('A'));
    assert_eq!(q.dequeue(), Some('B'));
    for x in ['D', 'E', 'F'] {
        q.enqueue(x).unwrap();
    }
    println!("head = {}, size = {}", q.head, q.size); // head = 2, size = 4
    assert_eq!(q.enqueue('G'), Err('G'));
    let out: Vec<char> = (0..4).map(|_| q.dequeue().unwrap()).collect();
    assert_eq!(out, vec!['C', 'D', 'E', 'F']);
    assert_eq!(q.dequeue(), None);
    println!("semua uji lolos");
}
