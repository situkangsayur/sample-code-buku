"""Bab 37: delta copy/insert ala packfile Git.

Delta dari base ke target berisi dua jenis instruksi:
    ("copy", offset, panjang)  salin potongan base
    ("insert", byte)           sisipkan byte baru
Encoder: index semua potongan K byte di base dengan hash table, lalu
untuk setiap posisi target cari kecocokan dan perpanjang secara greedy.
"""
K = 4


def buat_delta(base, target):
    index = {}
    for i in range(len(base) - K + 1):
        index.setdefault(base[i:i + K], i)       # posisi pertama cukup
    ops, i, sisip = [], 0, bytearray()
    while i < len(target):
        j = index.get(target[i:i + K])
        if j is None:
            sisip.append(target[i])
            i += 1
            continue
        panjang = K
        while (j + panjang < len(base) and i + panjang < len(target)
               and base[j + panjang] == target[i + panjang]):
            panjang += 1
        if sisip:
            ops.append(("insert", bytes(sisip)))
            sisip = bytearray()
        ops.append(("copy", j, panjang))
        i += panjang
    if sisip:
        ops.append(("insert", bytes(sisip)))
    return ops


def terapkan_delta(base, ops):
    out = bytearray()
    for op in ops:
        if op[0] == "copy":
            out += base[op[1]:op[1] + op[2]]
        else:
            out += op[1]
    return bytes(out)


def ukuran_delta(ops):
    """Taksiran byte: copy kira-kira 5 byte, insert 1 + panjang data."""
    return sum(5 if op[0] == "copy" else 1 + len(op[1]) for op in ops)


if __name__ == "__main__":
    v1 = b"def luas(p, l):\n    return p * l\n\nprint(luas(3, 4))\n"
    v2 = b"def luas(p, l):\n    # persegi panjang\n    return p * l\n\nprint(luas(5, 4))\n"
    ops = buat_delta(v1, v2)
    for op in ops:
        print(op)
    assert terapkan_delta(v1, ops) == v2

    base = b"".join(b"baris %04d isi file yang panjang\n" % i for i in range(500))
    target = base.replace(b"baris 0250", b"BARIS 0250") + b"baris tambahan\n"
    ops = buat_delta(base, target)
    assert terapkan_delta(base, ops) == target
    print("target %d byte, delta sekitar %d byte" % (len(target), ukuran_delta(ops)))
    assert ukuran_delta(ops) < len(target) // 100
    assert buat_delta(b"", b"abc") == [("insert", b"abc")]
    print("delta: semua uji lolos")
