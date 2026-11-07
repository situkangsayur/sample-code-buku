# Bab 7 - Hidden Markov Model

Contoh kode untuk Bab 7 buku *Fundamental Pembelajaran Mesin*. Semua contoh hanya
memerlukan NumPy; hmmlearn bersifat opsional.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `hmm_numpy.py` | Kode 7.2, 7.3, 7.4 | Modul HMM diskret dari nol: forward/backward (polos dan berskala), Viterbi di ruang log, Baum-Welch untuk banyak urutan, pembangkit data |
| `rantai_markov.py` | Kode 7.1 | Rantai Markov vokal/konsonan (data Markov 1913): matriks transisi, peluang n langkah, distribusi stasioner, simulasi |
| `contoh_tangan.py` | - | Semua angka contoh hitungan tangan (2 state, 3 simbol, T = 3): enumerasi, alpha, beta, gamma, Viterbi, satu iterasi Baum-Welch |
| `underflow.py` | - | Forward polos menghasilkan 0 untuk T panjang; versi berskala tetap benar; perbandingan ongkos enumerasi vs forward |
| `demo_regime.py` | Kode 7.5 | Baum-Welch pada 20 urutan sintetis, lima awal acak, akurasi Viterbi; menulis `riwayat_ll.csv` (data Gambar 7.7) |
| `gaussian_hmm.py` | Kode 7.6 | HMM emisi Gaussian 1D dari nol untuk regime return harian, dibandingkan dengan GMM tanpa urutan |
| `pos_tagging.py` | Kode 7.8 | POS tagging bahasa Indonesia dengan korpus mini: latih dengan menghitung, decode dengan Viterbi |
| `hmmlearn_opsional.py` | Kode 7.7 | Data regime yang sama dengan `GaussianHMM` dari hmmlearn (dilewati bila belum terpasang) |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python rantai_markov.py
python contoh_tangan.py
python underflow.py
python demo_regime.py
python gaussian_hmm.py
python pos_tagging.py
pip install hmmlearn        # opsional
python hmmlearn_opsional.py
```

Angka di buku dihasilkan dengan Python 3.12 dan NumPy 2.4 (hmmlearn 0.3.3 untuk contoh
opsional). Semua seed acak ditetapkan sehingga keluaran dapat diulang.
