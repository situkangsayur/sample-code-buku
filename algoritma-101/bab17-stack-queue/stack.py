"""Bab 17: stack berbasis list, pemeriksaan kurung, dan undo/redo dengan dua stack."""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):                # O(1) amortized
        self._items.append(x)

    def pop(self):                    # O(1)
        if not self._items:
            raise IndexError("pop dari stack kosong")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek dari stack kosong")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)


PAIRS = {")": "(", "]": "[", "}": "{"}


def balanced(text):
    """True bila setiap kurung buka punya pasangan tutup yang sesuai dan bersarang benar."""
    s = Stack()
    for ch in text:
        if ch in "([{":
            s.push(ch)
        elif ch in PAIRS:
            if s.is_empty() or s.pop() != PAIRS[ch]:
                return False
    return s.is_empty()


class Editor:
    """Teks dengan undo dan redo. Setiap aksi disimpan sebagai (jenis, isi)."""

    def __init__(self):
        self.text = ""
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def type(self, s):
        self.text += s
        self.undo_stack.push(("type", s))
        self.redo_stack = Stack()     # aksi baru menghapus riwayat redo

    def undo(self):
        if self.undo_stack.is_empty():
            return
        kind, s = self.undo_stack.pop()
        self.text = self.text[: len(self.text) - len(s)]
        self.redo_stack.push((kind, s))

    def redo(self):
        if self.redo_stack.is_empty():
            return
        kind, s = self.redo_stack.pop()
        self.text += s
        self.undo_stack.push((kind, s))


def main():
    s = Stack()
    for x in [1, 2, 3]:
        s.push(x)
    assert s.pop() == 3 and s.peek() == 2 and len(s) == 2

    cases = {"([]{})": True, "([)]": False, "((": False, "": True,
             "a[i] = f(b{c})": True, "}": False}
    for text, want in cases.items():
        assert balanced(text) == want, text
    print("([)] seimbang?", balanced("([)]"))   # False

    e = Editor()
    for w in ["Algo", "ritma", " 101"]:
        e.type(w)
    e.undo()
    e.undo()
    assert e.text == "Algo"
    e.redo()
    assert e.text == "Algoritma"
    e.type("!")
    e.redo()                          # tidak ada efek: riwayat redo sudah dihapus
    assert e.text == "Algoritma!"
    print("semua uji lolos")


if __name__ == "__main__":
    main()
