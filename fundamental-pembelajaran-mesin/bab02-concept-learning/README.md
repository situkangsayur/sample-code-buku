# Bab 2 - Concept Learning

Contoh kode untuk Bab 2 buku *Fundamental Pembelajaran Mesin*. Semua contoh Python hanya memakai
pustaka standar, sesuai semangat bab ini: algoritmanya cukup ditulis dengan `list` dan `for`.

| Berkas | Kode di buku | Isi |
|---|---|---|
| `enjoysport.csv` | - | Empat contoh latih EnjoySport (Mitchell, 1997, Tabel 2.1) |
| `find_s.py` | Kode 2.1 | Find-S dan klasifikasi hari baru |
| `candidate_elimination.py` | Kode 2.2 | Candidate-Elimination, mencetak S dan G setelah tiap contoh |
| `version_space_vote.py` | Kode 2.3 | List-Then-Eliminate: enumerasi 973 hipotesis, version space, dan voting |
| `rust-find-s/` | Kode 2.4 | Find-S dalam Rust |

## Menjalankan

```bash
python find_s.py
python candidate_elimination.py
python version_space_vote.py

cd rust-find-s && cargo run --release
```
