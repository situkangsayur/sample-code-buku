"""Bab 15: class dan object di Python, dengan contoh Point dan Circle."""
import math


class Point:
    """Titik di bidang dua dimensi."""

    def __init__(self, x, y):
        self.x = x                    # atribut milik setiap object
        self.y = y

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Shape:
    """Kelas dasar: setiap bentuk harus bisa menghitung luasnya."""

    def area(self):
        raise NotImplementedError

    def describe(self):
        return f"{type(self).__name__} dengan luas {self.area():.2f}"


class Circle(Shape):
    def __init__(self, center, r):
        self.center = center
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h


def main():
    p = Point(0, 0)
    q = Point(3, 4)
    print(p, q, p.distance(q))        # Point(0, 0) Point(3, 4) 5.0
    assert p.distance(q) == 5.0
    shapes = [Circle(p, 1), Rectangle(2, 3)]
    for s in shapes:
        print(s.describe())           # Circle dengan luas 3.14, Rectangle dengan luas 6.00
    assert shapes[1].describe() == "Rectangle dengan luas 6.00"
    r = q                             # r dan q menunjuk object yang sama
    r.x = 10
    assert q.x == 10
    print("semua uji lolos")


if __name__ == "__main__":
    main()
