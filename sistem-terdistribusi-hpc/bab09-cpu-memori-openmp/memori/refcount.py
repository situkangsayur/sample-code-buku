"""Kode 9.4: reference counting dan cycle collector di CPython."""
import gc
import sys

a = [1, 2, 3]
b = a
print("refcount a:", sys.getrefcount(a))   # a, b, dan argumen getrefcount


class Simpul:
    def __init__(self):
        self.lain = None


gc.disable()                 # agar terlihat jelas kapan siklus dipungut
x, y = Simpul(), Simpul()
x.lain, y.lain = y, x        # siklus: x -> y -> x
del x, y                     # hitungan referensi tidak pernah nol
print("objek tak terjangkau yang dipungut:", gc.collect())
gc.enable()
