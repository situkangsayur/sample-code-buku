# Bab 5: Flowchart dan Diagram Nassi-Shneiderman

Kode pendamping Bab 5 buku *Algoritma 101*.

| File | Isi | Kaitan di buku |
|---|---|---|
| `maks3.py` | maksimum tiga bilangan, rata-rata n nilai, potongan harga | Algoritma 5.1 dan 5.2, Gambar 5.2 dan 5.3 |
| `jumlah_positif.py` | menjumlahkan bilangan positif sampai 0, versi terstruktur dan versi "kusut" | Algoritma 5.3, Kode 5.1, Gambar 5.4 |
| `jumlah_positif.mmd` | flowchart Gambar 5.4(b) dalam sintaks Mermaid | Kode 5.3 |
| `rust/src/bin/jumlah_positif.rs` | JumlahPositif di Rust | Kode 5.2 |
| `rust/src/bin/maks3.rs` | Maks3 di Rust | Latihan 10 |

Menjalankan:

```
python3 maks3.py
python3 jumlah_positif.py
cd rust && cargo test && cargo run --bin jumlah_positif && cargo run --bin maks3
```

Berkas `.mmd` dapat ditempel ke blok kode bertanda `mermaid` di Markdown GitHub, atau dibuka di
Mermaid Live Editor.
