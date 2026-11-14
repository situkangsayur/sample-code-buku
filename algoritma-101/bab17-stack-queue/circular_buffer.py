"""Bab 17: queue berkapasitas tetap dengan circular buffer (head, size, mod)."""


class CircularQueue:
    def __init__(self, capacity):
        self.buf = [None] * capacity
        self.cap = capacity
        self.head = 0                 # indeks elemen terdepan
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.cap

    def enqueue(self, x):             # O(1)
        if self.is_full():
            raise OverflowError("queue penuh")
        tail = (self.head + self.size) % self.cap
        self.buf[tail] = x
        self.size += 1

    def dequeue(self):                # O(1)
        if self.is_empty():
            raise IndexError("queue kosong")
        x = self.buf[self.head]
        self.buf[self.head] = None
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x

    def front(self):
        if self.is_empty():
            raise IndexError("queue kosong")
        return self.buf[self.head]


def main():
    q = CircularQueue(4)
    for x in "ABC":
        q.enqueue(x)
    assert q.dequeue() == "A" and q.dequeue() == "B"
    for x in "DEF":
        q.enqueue(x)                  # tail berputar kembali ke indeks 0 dan 1
    print("buf:", q.buf, "head:", q.head, "size:", q.size)
    # buf: ['E', 'F', 'C', 'D'] head: 2 size: 4
    assert q.buf == ["E", "F", "C", "D"] and q.head == 2 and q.is_full()
    try:
        q.enqueue("G")
        assert False
    except OverflowError:
        pass
    assert [q.dequeue() for _ in range(4)] == ["C", "D", "E", "F"]
    assert q.is_empty()
    print("semua uji lolos")


if __name__ == "__main__":
    main()
