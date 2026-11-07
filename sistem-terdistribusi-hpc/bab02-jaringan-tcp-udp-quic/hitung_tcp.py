"""Hitungan Bab 2: overhead, RTO (Algoritma 2.2), BDP, Mathis, waktu transfer."""
import math


def rto_rfc6298(sampel, alpha=1 / 8, beta=1 / 4, k=4):
    srtt = rttvar = None
    for r in sampel:
        if srtt is None:
            srtt, rttvar = r, r / 2
        else:
            rttvar = (1 - beta) * rttvar + beta * abs(srtt - r)
            srtt = (1 - alpha) * srtt + alpha * r
        yield r, srtt, rttvar, srtt + k * rttvar


print("RTO untuk sampel 100, 140 ms:")
for r, s, v, rto in rto_rfc6298([100, 140]):
    print(f"  R={r} SRTT={s:.1f} RTTVAR={v:.1f} RTO={rto:.1f}")

bdp = 100e6 * 0.1 / 8
print(f"BDP 100 Mbps x 100 ms = {bdp / 1e6:.2f} MB")
print(f"throughput window 64 KB, RTT 100 ms = {65535 / 0.1 * 8 / 1e6:.1f} Mbps")

mss, rtt, p = 1460, 0.1, 0.01
print(f"Mathis: {mss / rtt * 1.22 / math.sqrt(p) * 8 / 1e6:.2f} Mbps")

for L in (1e4, 1e9):
    t = 0.3 + 8 * L / 1e9
    print(f"transfer {L:.0e} B, RTT 200 ms, 1 Gbps: {t:.4f} s")
print(f"overhead pesan 8 B lewat TCP/Ethernet: {8 / (14 + 20 + 20 + 8 + 4):.1%} muatan")
print(f"ping UDP hilang bila loss 5% per arah: {1 - 0.95 ** 2:.2%}")
