"""Closest pair of points dengan divide and conquer."""
import math
import random


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def brute(pts):
    best = math.inf
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            best = min(best, dist(pts[i], pts[j]))
    return best


def closest_rec(px, py):
    """px terurut menurut x, py titik yang sama terurut menurut y."""
    n = len(px)
    if n <= 3:
        return brute(px)
    mid = n // 2
    xm = px[mid][0]
    left_set = set(px[:mid])
    py_l = [p for p in py if p in left_set]
    py_r = [p for p in py if p not in left_set]
    d = min(closest_rec(px[:mid], py_l), closest_rec(px[mid:], py_r))
    strip = [p for p in py if abs(p[0] - xm) < d]   # pita selebar 2d
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < d:
            d = min(d, dist(strip[i], strip[j]))
            j += 1
    return d


def closest_pair(points):
    pts = list(set(points))
    if len(pts) < len(points):
        return 0.0                          # ada titik kembar
    px = sorted(pts)
    py = sorted(pts, key=lambda p: p[1])
    return closest_rec(px, py)


if __name__ == "__main__":
    titik = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print(round(closest_pair(titik), 4))     # 1.4142, pasangan (2,3)-(3,4)
    assert abs(closest_pair(titik) - math.sqrt(2)) < 1e-9
    for _ in range(300):
        n = random.randint(2, 80)
        pts = [(random.randint(0, 200), random.randint(0, 200)) for _ in range(n)]
        assert abs(closest_pair(pts) - brute(pts)) < 1e-9
    print("semua uji closest pair lolos")
