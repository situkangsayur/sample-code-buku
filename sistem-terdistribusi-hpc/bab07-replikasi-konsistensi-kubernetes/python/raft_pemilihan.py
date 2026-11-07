"""Simulasi sederhana pemilihan leader Raft (Algoritma 7.2) dalam waktu diskret.

Bukan implementasi Raft lengkap: hanya election timeout acak, RequestVote,
satu suara per term, dan heartbeat. Cukup untuk melihat mengapa timeout acak
biasanya menghasilkan satu leader dengan cepat, dan apa yang terjadi saat leader mati.
Pemakaian: python raft_pemilihan.py [jumlah_node] [seed]
"""
import random, sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 3)
HB, TMIN, TMAX = 50, 150, 300            # ms, sesuai makalah Raft


class Node:
    def __init__(self, i):
        self.i, self.term, self.voted, self.peran, self.hidup = i, 0, None, "follower", True
        self.reset()

    def reset(self):
        self.batas = sekarang + random.randint(TMIN, TMAX)


def mayoritas():
    return N // 2 + 1


sekarang = 0
nodes = [Node(i) for i in range(N)]
for t in range(0, 2000):
    sekarang = t
    if t == 1000:                         # matikan leader di tengah simulasi
        for n in nodes:
            if n.peran == "leader":
                n.hidup = False
                print(f"{t:5d} ms  leader N{n.i} MATI")
    for n in nodes:
        if not n.hidup:
            continue
        if n.peran == "leader" and t % HB == 0:          # heartbeat
            for m in nodes:
                if m is not n and m.hidup and m.term <= n.term:
                    m.term, m.peran = n.term, "follower"
                    m.reset()
        elif n.peran != "leader" and t >= n.batas:        # election timeout habis
            n.term += 1; n.peran = "candidate"; n.voted = n.i; n.reset()
            suara = 1
            for m in nodes:
                if m is n or not m.hidup:
                    continue
                if n.term > m.term:
                    m.term, m.voted, m.peran = n.term, None, "follower"
                if m.term == n.term and m.voted in (None, n.i):
                    m.voted = n.i; m.reset(); suara += 1
            print(f"{t:5d} ms  N{n.i} mencalonkan diri di term {n.term}: {suara}/{N} suara")
            if suara >= mayoritas():
                n.peran = "leader"
                print(f"{t:5d} ms  N{n.i} menjadi LEADER term {n.term}")
