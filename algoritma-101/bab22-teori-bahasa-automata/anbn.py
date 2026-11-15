"""Pengenal bahasa a^n b^n dengan satu stack (Algoritma 22.2).

Bahasa ini context-free tetapi tidak regular. Stack dipakai untuk
mengingat banyaknya a yang belum dipasangkan dengan b.
"""


def terima_anbn(w):
    stack = []
    fase_b = False
    for c in w:
        if c == "a":
            if fase_b:
                return False      # a muncul sesudah b
            stack.append("A")
        elif c == "b":
            fase_b = True
            if not stack:
                return False      # b lebih banyak dari a
            stack.pop()
        else:
            return False          # simbol di luar alfabet
    return len(stack) == 0


if __name__ == "__main__":
    print(terima_anbn("aaabbb"))  # True
    print(terima_anbn("aabbb"))   # False
    print(terima_anbn("abab"))    # False
    for n in range(0, 30):
        assert terima_anbn("a" * n + "b" * n)
        assert not terima_anbn("a" * (n + 1) + "b" * n)
        assert not terima_anbn("a" * n + "b" * (n + 1))
    assert not terima_anbn("ba")
    print("semua uji lolos")
