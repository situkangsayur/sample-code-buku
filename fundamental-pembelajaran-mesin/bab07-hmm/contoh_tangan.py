"""Contoh hitungan tangan Bab 7: HMM 2 state, 3 simbol, T = 3.

State : 0 = Tenang, 1 = Gejolak
Simbol: 0 = Naik, 1 = Datar, 2 = Turun
Urutan: O = (Datar, Turun, Turun)
"""
import itertools
import numpy as np
from hmm_numpy import forward, backward, viterbi_log, baum_welch

STATE = ["Tenang", "Gejolak"]
SIMBOL = ["Naik", "Datar", "Turun"]
A = np.array([[0.8, 0.2],
              [0.3, 0.7]])
B = np.array([[0.3, 0.6, 0.1],
              [0.4, 0.1, 0.5]])
pi = np.array([0.6, 0.4])
O = np.array([1, 2, 2])

np.set_printoptions(precision=6, suppress=True)
print("Urutan:", [SIMBOL[k] for k in O])

# 1. Enumerasi naif: semua N^T = 8 lintasan
print("\n[1] Enumerasi semua lintasan")
total = 0.0
for Q in itertools.product(range(2), repeat=len(O)):
    p = pi[Q[0]] * B[Q[0], O[0]]
    for t in range(1, len(O)):
        p *= A[Q[t - 1], Q[t]] * B[Q[t], O[t]]
    total += p
    print(" ", "-".join(STATE[q][0] for q in Q), f"{p:.6f}")
print(f"  jumlah = P(O|lambda) = {total:.6f}")

# 2. Forward
alpha, pO = forward(A, B, pi, O)
print("\n[2] alpha (baris = t, kolom = Tenang, Gejolak)\n", alpha)
print(f"  P(O|lambda) = {pO:.6f}")

# 3. Backward
beta = backward(A, B, O)
print("\n[3] beta\n", beta)
print("  cek sum_i pi_i b_i(o1) beta_1(i) =",
      f"{(pi * B[:, O[0]] * beta[0]).sum():.6f}")

# 4. Posterior gamma
gamma = alpha * beta / pO
print("\n[4] gamma = P(q_t = i | O)\n", gamma)
print("  posterior decoding:", [STATE[i] for i in gamma.argmax(axis=1)])

# 5. Viterbi (versi polos agar angkanya mudah dibaca)
T, N = len(O), 2
delta = np.zeros((T, N)); psi = np.zeros((T, N), dtype=int)
delta[0] = pi * B[:, O[0]]
for t in range(1, T):
    skor = delta[t - 1][:, None] * A
    psi[t] = skor.argmax(axis=0)
    delta[t] = skor.max(axis=0) * B[:, O[t]]
print("\n[5] delta\n", delta)
print("  psi\n", psi)
q, lp = viterbi_log(A, B, pi, O)
print("  lintasan Viterbi:", [STATE[i] for i in q], f"P* = {np.exp(lp):.6f}")

# 6. Satu iterasi Baum-Welch pada urutan yang sama
A1, B1, pi1, ll = baum_welch([O], 2, 3, n_iter=2, tol=0, init=(A, B, pi))
print("\n[6] log P(O) iterasi 0 dan 1:", [f"{x:.6f}" for x in ll])
print("  P(O) sebelum/sesudah:", [f"{np.exp(x):.6f}" for x in ll])
A1, B1, pi1, _ = baum_welch([O], 2, 3, n_iter=1, tol=0, init=(A, B, pi))
print("  pi baru:", pi1)
print("  A baru:\n", A1)
print("  B baru:\n", B1)
