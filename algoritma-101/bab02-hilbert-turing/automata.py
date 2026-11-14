"""Bab 2: finite automata dan pemeriksa kurung dengan stack.

1. DFA yang menerima bilangan biner yang habis dibagi 3.
   State = sisa bagi 3 dari bagian yang sudah dibaca.
   Membaca bit b dari state r membawa ke state (2r + b) mod 3.
2. Pemeriksa kurung seimbang, gambaran pushdown automata.
"""


def dfa_kelipatan_tiga(s, jejak=None):
    r = 0  # state awal q0
    for b in s:
        r_baru = (2 * r + int(b)) % 3
        if jejak is not None:
            jejak.append((r, b, r_baru))
        r = r_baru
    return r == 0  # q0 adalah state penerima


def kurung_seimbang(s):
    stack = []
    for c in s:
        if c == "(":
            stack.append(c)
        elif c == ")":
            if not stack:
                return False
            stack.pop()
    return not stack


if __name__ == "__main__":
    jejak = []
    assert dfa_kelipatan_tiga("1100", jejak)  # 12
    print(jejak)
    assert jejak == [(0, "1", 1), (1, "1", 0), (0, "0", 0), (0, "0", 0)]
    for n in range(0, 500):
        assert dfa_kelipatan_tiga(format(n, "b")) == (n % 3 == 0)
    assert kurung_seimbang("(()())")
    assert not kurung_seimbang("(()")
    assert not kurung_seimbang("())(")
    print("semua uji lolos")
