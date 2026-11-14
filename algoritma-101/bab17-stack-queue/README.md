# Bab 17: Stack dan Queue

| File | Isi | Kaitan di buku |
|---|---|---|
| `call_stack_demo.py` | Rekursi melampaui batas call stack Python dan versi iteratif | Kode 17.1 |
| `stack.py` | Class `Stack`, pemeriksaan kurung, editor dengan undo/redo | Algoritma 17.1, 17.2; Kode 17.2; Tabel 17.2 |
| `circular_buffer.py` | Queue berkapasitas tetap dengan circular buffer | Algoritma 17.3; Kode 17.4; Tabel 17.4 |
| `deque_demo.py` | `collections.deque`, `maxlen`, maksimum jendela geser, pengukuran `list.pop(0)` vs `deque.popleft()` | Algoritma 17.4; Kode 17.5; Subbab 17.3 |
| `rust/src/bin/stack.rs` | `Vec` sebagai stack, pemeriksaan kurung | Kode 17.3 |
| `rust/src/bin/circular_buffer.rs` | Circular buffer generik dengan `Result` | Subbab 17.4 |
| `rust/src/bin/deque.rs` | `VecDeque` dan maksimum jendela geser, diuji terhadap solusi naif | Subbab 17.4 |

Menjalankan:

```
for f in call_stack_demo stack circular_buffer deque_demo; do python3 $f.py; done
cd rust && cargo test && for b in stack circular_buffer deque; do cargo run --bin $b; done
```
