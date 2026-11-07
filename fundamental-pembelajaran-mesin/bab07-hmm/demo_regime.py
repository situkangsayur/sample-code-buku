"""Baum-Welch pada data sintetis regime pasar (Tenang/Gejolak, simbol Naik/Datar/Turun)."""
import numpy as np
from hmm_numpy import baum_welch, viterbi_log, forward_scaled, sample

A = np.array([[0.8, 0.2], [0.3, 0.7]])
B = np.array([[0.3, 0.6, 0.1], [0.4, 0.1, 0.5]])
pi = np.array([0.6, 0.4])

rng = np.random.default_rng(2026)
# 20 urutan masing-masing 100 hari
data = [sample(A, B, pi, 100, rng) for _ in range(20)]
Q_list = [q for q, _ in data]
O_list = [o for _, o in data]
ll_benar = sum(forward_scaled(A, B, pi, o)[2] for o in O_list)
print(f"log-likelihood model sebenarnya: {ll_benar:.2f}")

# Beberapa awal acak; EM hanya menjamin optimum lokal
hasil = []
for seed in range(5):
    A_, B_, pi_, ll = baum_welch(O_list, 2, 3, n_iter=500, tol=1e-6, seed=seed)
    hasil.append((ll[-1], seed, A_, B_, pi_, ll))
    print(f"seed {seed}: iterasi {len(ll):3d}, log-likelihood akhir {ll[-1]:.2f}")

ll_akhir, seed, A_, B_, pi_, ll = max(hasil, key=lambda h: h[0])
# Label state hasil EM bisa tertukar: urutkan agar state 0 = yang paling sering 'Datar'
urut = np.argsort(-B_[:, 1])
A_, B_, pi_ = A_[np.ix_(urut, urut)], B_[urut], pi_[urut]
np.set_printoptions(precision=3, suppress=True)
print(f"\nterbaik: seed {seed}")
print("A taksiran:\n", A_)
print("B taksiran:\n", B_)
print("riwayat log-likelihood (iterasi 0,1,2,5,10,20,50,akhir):")
for i in (0, 1, 2, 5, 10, 20, 50, len(ll) - 1):
    if i < len(ll):
        print(f"  {i:3d}: {ll[i]:.2f}")

# Akurasi Viterbi terhadap state sebenarnya
benar = total = 0
for q, o in zip(Q_list, O_list):
    qh, _ = viterbi_log(A_, B_, pi_, o)
    benar += (qh == q).sum(); total += len(q)
qb = sum((viterbi_log(A, B, pi, o)[0] == q).sum() for q, o in zip(Q_list, O_list))
print(f"akurasi Viterbi (model taksiran): {benar / total:.3f}")
print(f"akurasi Viterbi (model sebenarnya): {qb / total:.3f}")

# Simpan riwayat semua seed untuk grafik (kolom kosong bila sudah konvergen)
n = max(len(h[5]) for h in hasil)
with open("riwayat_ll.csv", "w") as f:
    f.write("iterasi," + ",".join(f"seed{h[1]}" for h in hasil) + "\n")
    for i in range(n):
        f.write(str(i) + "," + ",".join(f"{h[5][i]:.2f}" if i < len(h[5]) else ""
                                        for h in hasil) + "\n")
