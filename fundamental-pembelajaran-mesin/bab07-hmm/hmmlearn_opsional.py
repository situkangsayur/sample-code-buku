"""Opsional: data regime yang sama dengan gaussian_hmm.py, dilatih dengan hmmlearn.

hmmlearn tidak wajib. Pasang dengan: pip install hmmlearn
"""
import sys
import numpy as np

try:
    from hmmlearn import hmm
except ImportError:
    print("hmmlearn belum terpasang; lewati contoh ini (pip install hmmlearn).")
    sys.exit(0)

# Bangkitkan data yang sama persis dengan gaussian_hmm.py
rng = np.random.default_rng(11)
A0 = np.array([[0.98, 0.02], [0.05, 0.95]])
mu0, sd0 = np.array([0.05, -0.10]), np.array([0.6, 1.8])
q = np.zeros(1000, int)
for t in range(1, 1000):
    q[t] = rng.choice(2, p=A0[q[t - 1]])
x = rng.normal(mu0[q], sd0[q]).reshape(-1, 1)    # hmmlearn meminta bentuk (T, fitur)

model = hmm.GaussianHMM(n_components=2, covariance_type="diag",
                        n_iter=200, tol=1e-6, random_state=0)
model.fit(x)
qh = model.predict(x)                            # Viterbi
urut = np.argsort(model.covars_.ravel())         # state 0 = varians kecil (Tenang)
qh = np.argsort(urut)[qh]
np.set_printoptions(precision=3, suppress=True)
print("konvergen:", model.monitor_.converged, " iterasi:", model.monitor_.iter)
print("log-likelihood:", round(model.score(x), 2))
print("A:\n", model.transmat_[np.ix_(urut, urut)])
print("mu:", model.means_.ravel()[urut], " sd:", np.sqrt(model.covars_.ravel()[urut]))
print("akurasi Viterbi:", round((qh == q).mean(), 3))
