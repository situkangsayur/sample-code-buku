"""HMM dengan emisi Gaussian 1D dari nol, dibandingkan dengan GMM (tanpa urutan).

Data sintetis: return harian (%) dari dua regime.
  Tenang : rata-rata  0.05, simpangan baku 0.6
  Gejolak: rata-rata -0.10, simpangan baku 1.8
"""
import numpy as np


def norm_pdf(x, mu, sd):
    return np.exp(-0.5 * ((x[:, None] - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def fb_scaled(A, pi, L):
    """Forward-backward berskala dengan matriks likelihood emisi L (T x N)."""
    T, N = L.shape
    alpha, beta, c = np.zeros((T, N)), np.zeros((T, N)), np.zeros(T)
    a = pi * L[0]; c[0] = 1 / a.sum(); alpha[0] = a * c[0]
    for t in range(1, T):
        a = (alpha[t - 1] @ A) * L[t]; c[t] = 1 / a.sum(); alpha[t] = a * c[t]
    beta[-1] = c[-1]
    for t in range(T - 2, -1, -1):
        beta[t] = (A @ (L[t + 1] * beta[t + 1])) * c[t]
    return alpha, beta, c, -np.log(c).sum()


def fit_ghmm(x, N=2, n_iter=200, tol=1e-6):
    # Inisialisasi dari kuantil data: state 0 sempit, state 1 lebar
    mu = np.full(N, x.mean()); sd = np.array([0.5, 2.0]) * x.std()
    A = np.full((N, N), 0.1 / (N - 1)); np.fill_diagonal(A, 0.9)
    pi = np.full(N, 1 / N); ll_lama = -np.inf
    for it in range(n_iter):
        L = norm_pdf(x, mu, sd)
        alpha, beta, c, ll = fb_scaled(A, pi, L)
        gamma = alpha * beta / c[:, None]                      # langkah E
        xi = alpha[:-1, :, None] * A[None] * (L[1:] * beta[1:])[:, None, :]
        pi = gamma[0]                                          # langkah M
        A = xi.sum(0) / xi.sum((0, 2))[:, None]
        w = gamma.sum(0)
        mu = (gamma * x[:, None]).sum(0) / w
        sd = np.sqrt((gamma * (x[:, None] - mu) ** 2).sum(0) / w)
        if ll - ll_lama < tol:
            break
        ll_lama = ll
    return A, mu, sd, pi, ll, it + 1


def viterbi_L(A, pi, L):
    T, N = L.shape
    lA, lL = np.log(A), np.log(L)
    d = np.log(pi) + lL[0]; psi = np.zeros((T, N), int)
    for t in range(1, T):
        s = d[:, None] + lA; psi[t] = s.argmax(0); d = s.max(0) + lL[t]
    q = np.zeros(T, int); q[-1] = d.argmax()
    for t in range(T - 2, -1, -1):
        q[t] = psi[t + 1, q[t + 1]]
    return q


def fit_gmm(x, n_iter=500, tol=1e-6):
    """GMM 1D dua komponen (EM, Bab GMM): sama dengan HMM tanpa transisi."""
    w = np.array([0.5, 0.5]); mu = np.full(2, x.mean()); sd = np.array([0.5, 2.0]) * x.std()
    ll_lama = -np.inf
    for _ in range(n_iter):
        p = w * norm_pdf(x, mu, sd); ll = np.log(p.sum(1)).sum()
        r = p / p.sum(1, keepdims=True)
        n = r.sum(0); w = n / len(x)
        mu = (r * x[:, None]).sum(0) / n
        sd = np.sqrt((r * (x[:, None] - mu) ** 2).sum(0) / n)
        if ll - ll_lama < tol:
            break
        ll_lama = ll
    return w, mu, sd, r


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    A0 = np.array([[0.98, 0.02], [0.05, 0.95]])
    mu0, sd0 = np.array([0.05, -0.10]), np.array([0.6, 1.8])
    T = 1000
    q = np.zeros(T, int)
    for t in range(1, T):
        q[t] = rng.choice(2, p=A0[q[t - 1]])
    x = rng.normal(mu0[q], sd0[q])
    print(f"hari di regime Gejolak: {q.mean():.3f}, jumlah pergantian regime: {(np.diff(q) != 0).sum()}")

    A, mu, sd, pi, ll, n_it = fit_ghmm(x)
    np.set_printoptions(precision=3, suppress=True)
    print(f"\nHMM Gaussian ({n_it} iterasi, log-likelihood {ll:.2f})")
    print("A:\n", A); print("mu:", mu, " sd:", sd)
    qh = viterbi_L(A, pi, norm_pdf(x, mu, sd))
    print(f"akurasi Viterbi: {(qh == q).mean():.3f}, pergantian regime ditebak: {(np.diff(qh) != 0).sum()}")

    w, mug, sdg, r = fit_gmm(x)
    qg = r.argmax(1)
    print(f"\nGMM: w={w}, mu={mug}, sd={sdg}")
    print(f"akurasi GMM per hari: {(qg == q).mean():.3f}, pergantian regime ditebak: {(np.diff(qg) != 0).sum()}")
