"""HMM diskret dari nol dengan NumPy (Bab 7, Hidden Markov Model).

Notasi mengikuti Rabiner (1989):
  A[i, j] = P(q_{t+1} = j | q_t = i)    matriks transisi N x N
  B[j, k] = P(o_t = k | q_t = j)        matriks emisi N x M
  pi[i]   = P(q_1 = i)                  distribusi awal
  O       = array indeks simbol 0..M-1, panjang T

Fungsi:
  forward / backward          versi polos (untuk contoh kecil dan hitungan tangan)
  forward_scaled / backward_scaled   versi berskala (aman untuk T panjang)
  viterbi_log                 decoding di ruang log
  baum_welch                  pelatihan EM (versi berskala), bisa banyak urutan
  sample                      membangkitkan urutan dari model
"""
import numpy as np


# ---------------------------------------------------------------------------
# Evaluasi: forward dan backward (polos)
# ---------------------------------------------------------------------------
def forward(A, B, pi, O):
    """Kembalikan matriks alpha (T x N) dan P(O | lambda)."""
    T, N = len(O), A.shape[0]
    alpha = np.zeros((T, N))
    alpha[0] = pi * B[:, O[0]]                       # inisialisasi
    for t in range(1, T):                            # induksi
        alpha[t] = (alpha[t - 1] @ A) * B[:, O[t]]
    return alpha, alpha[-1].sum()                    # terminasi


def backward(A, B, O):
    """Kembalikan matriks beta (T x N)."""
    T, N = len(O), A.shape[0]
    beta = np.zeros((T, N))
    beta[-1] = 1.0
    for t in range(T - 2, -1, -1):
        beta[t] = A @ (B[:, O[t + 1]] * beta[t + 1])
    return beta


# ---------------------------------------------------------------------------
# Evaluasi berskala (Rabiner 1989, Bagian V.A)
# ---------------------------------------------------------------------------
def forward_scaled(A, B, pi, O):
    """alpha_hat (T x N) yang tiap barisnya berjumlah 1, faktor skala c,
    dan log P(O | lambda) = -sum(log c)."""
    T, N = len(O), A.shape[0]
    alpha = np.zeros((T, N))
    c = np.zeros(T)
    a = pi * B[:, O[0]]
    c[0] = 1.0 / a.sum()
    alpha[0] = a * c[0]
    for t in range(1, T):
        a = (alpha[t - 1] @ A) * B[:, O[t]]
        c[t] = 1.0 / a.sum()
        alpha[t] = a * c[t]
    return alpha, c, -np.log(c).sum()


def backward_scaled(A, B, O, c):
    """beta_hat memakai faktor skala c yang sama dengan forward_scaled."""
    T, N = len(O), A.shape[0]
    beta = np.zeros((T, N))
    beta[-1] = c[-1]
    for t in range(T - 2, -1, -1):
        beta[t] = (A @ (B[:, O[t + 1]] * beta[t + 1])) * c[t]
    return beta


# ---------------------------------------------------------------------------
# Decoding: Viterbi di ruang log
# ---------------------------------------------------------------------------
def viterbi_log(A, B, pi, O):
    """Kembalikan lintasan state terbaik dan log peluangnya."""
    T, N = len(O), A.shape[0]
    with np.errstate(divide="ignore"):               # log(0) = -inf, aman
        lA, lB, lpi = np.log(A), np.log(B), np.log(pi)
    delta = np.zeros((T, N))
    psi = np.zeros((T, N), dtype=int)
    delta[0] = lpi + lB[:, O[0]]
    for t in range(1, T):
        skor = delta[t - 1][:, None] + lA            # skor[i, j]: dari i ke j
        psi[t] = skor.argmax(axis=0)
        delta[t] = skor.max(axis=0) + lB[:, O[t]]
    q = np.zeros(T, dtype=int)
    q[-1] = delta[-1].argmax()
    for t in range(T - 2, -1, -1):                   # backtracking
        q[t] = psi[t + 1, q[t + 1]]
    return q, delta[-1].max()


# ---------------------------------------------------------------------------
# Learning: Baum-Welch (EM) berskala, untuk satu atau banyak urutan
# ---------------------------------------------------------------------------
def e_step(A, B, pi, O):
    """gamma (T x N), jumlah xi atas t (N x N), dan log-likelihood satu urutan."""
    alpha, c, ll = forward_scaled(A, B, pi, O)
    beta = backward_scaled(A, B, O, c)
    gamma = alpha * beta / c[:, None]                # baris berjumlah 1
    xi_sum = np.zeros_like(A)
    for t in range(len(O) - 1):
        xi_sum += alpha[t][:, None] * A * (B[:, O[t + 1]] * beta[t + 1])[None, :]
    return gamma, xi_sum, ll


def m_step(O_list, A, B, pi):
    """Satu putaran EM: langkah E pada semua urutan, lalu langkah M.
    Kembalikan parameter baru dan log-likelihood parameter lama."""
    N, M = B.shape
    A_num, B_num, pi_num, ll = np.zeros((N, N)), np.zeros((N, M)), np.zeros(N), 0.0
    for O in O_list:
        gamma, xi_sum, ll_r = e_step(A, B, pi, O)
        ll += ll_r
        pi_num += gamma[0]; A_num += xi_sum
        for k in range(M):
            B_num[:, k] += gamma[O == k].sum(axis=0)
    return (A_num / A_num.sum(1, keepdims=True),
            B_num / B_num.sum(1, keepdims=True), pi_num / pi_num.sum(), ll)


def baum_welch(O_list, N, M, n_iter=100, tol=1e-6, seed=0, init=None, verbose=False):
    """Latih HMM diskret. O_list: list array simbol. Kembalikan (A, B, pi, riwayat_ll)."""
    rng = np.random.default_rng(seed)
    if init is None:
        A = rng.dirichlet(np.ones(N), size=N)
        B = rng.dirichlet(np.ones(M), size=N)
        pi = rng.dirichlet(np.ones(N))
    else:
        A, B, pi = (np.array(x, dtype=float) for x in init)
    riwayat = []
    for it in range(n_iter):
        A, B, pi, ll = m_step(O_list, A, B, pi)       # ll milik parameter lama
        riwayat.append(ll)
        if verbose:
            print(f"iterasi {it:3d}  log P(O|lambda) = {ll:.6f}")
        if it > 0 and abs(riwayat[-1] - riwayat[-2]) < tol:
            break
    return A, B, pi, riwayat


# ---------------------------------------------------------------------------
# Membangkitkan data
# ---------------------------------------------------------------------------
def sample(A, B, pi, T, rng):
    """Bangkitkan (state, observasi) sepanjang T."""
    N, M = B.shape
    q = np.zeros(T, dtype=int)
    o = np.zeros(T, dtype=int)
    q[0] = rng.choice(N, p=pi)
    o[0] = rng.choice(M, p=B[q[0]])
    for t in range(1, T):
        q[t] = rng.choice(N, p=A[q[t - 1]])
        o[t] = rng.choice(M, p=B[q[t]])
    return q, o
