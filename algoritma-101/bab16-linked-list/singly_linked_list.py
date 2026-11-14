"""Bab 16: single linked list dengan head dan tail."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next              # None berperan sebagai nil


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def push_front(self, value):      # O(1)
        node = Node(value, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def push_back(self, value):       # O(1) karena ada tail
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def find(self, value):            # O(n)
        p = self.head
        while p is not None and p.value != value:
            p = p.next
        return p

    def insert_after(self, node, value):   # O(1) bila node sudah diketahui
        new = Node(value, node.next)
        node.next = new
        if self.tail is node:
            self.tail = new
        self.size += 1

    def delete(self, value):          # O(n): cari pendahulu lebih dulu
        prev, p = None, self.head
        while p is not None and p.value != value:
            prev, p = p, p.next
        if p is None:
            return False
        if prev is None:
            self.head = p.next
        else:
            prev.next = p.next
        if self.tail is p:
            self.tail = prev
        self.size -= 1
        return True

    def reverse(self):                # O(n), ruang tambahan O(1)
        prev, p = None, self.head
        self.tail = self.head
        while p is not None:
            nxt = p.next
            p.next = prev
            prev, p = p, nxt
        self.head = prev

    def __iter__(self):
        p = self.head
        while p is not None:
            yield p.value
            p = p.next

    def __len__(self):
        return self.size


def main():
    s = SinglyLinkedList()
    for v in [20, 30]:
        s.push_back(v)
    s.push_front(10)
    print(list(s))                    # [10, 20, 30]
    assert list(s) == [10, 20, 30]
    s.insert_after(s.find(20), 25)
    assert list(s) == [10, 20, 25, 30]
    assert s.delete(10) and s.delete(30) and not s.delete(99)
    assert list(s) == [20, 25] and s.tail.value == 25
    s.push_back(40)
    s.reverse()
    assert list(s) == [40, 25, 20] and s.tail.value == 20 and len(s) == 3
    e = SinglyLinkedList()
    e.reverse()
    assert list(e) == [] and not e.delete(1)
    print("semua uji lolos")


if __name__ == "__main__":
    main()
