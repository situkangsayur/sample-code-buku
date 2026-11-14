"""Bab 16: double linked list dengan dua sentinel (head dan tail palsu).

Sentinel membuat sisip dan hapus tidak perlu kasus khusus untuk list kosong.
"""


class DNode:
    def __init__(self, value=None):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = DNode()           # sentinel depan
        self.tail = DNode()           # sentinel belakang
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def insert_after(self, node, value):   # O(1)
        new = DNode(value)
        new.prev = node
        new.next = node.next
        node.next.prev = new
        node.next = new
        self.size += 1
        return new

    def push_front(self, value):
        return self.insert_after(self.head, value)

    def push_back(self, value):
        return self.insert_after(self.tail.prev, value)

    def remove(self, node):           # O(1) bila node sudah diketahui
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None
        self.size -= 1
        return node.value

    def forward(self):
        p = self.head.next
        while p is not self.tail:
            yield p.value
            p = p.next

    def backward(self):
        p = self.tail.prev
        while p is not self.head:
            yield p.value
            p = p.prev


def main():
    d = DoublyLinkedList()
    a = d.push_back("A")
    c = d.push_back("C")
    d.insert_after(a, "B")
    d.push_front("S")
    print(list(d.forward()), list(d.backward()))
    assert list(d.forward()) == ["S", "A", "B", "C"]
    assert list(d.backward()) == ["C", "B", "A", "S"]
    assert d.remove(c) == "C"
    assert list(d.forward()) == ["S", "A", "B"] and d.size == 3
    print("semua uji lolos")


if __name__ == "__main__":
    main()
