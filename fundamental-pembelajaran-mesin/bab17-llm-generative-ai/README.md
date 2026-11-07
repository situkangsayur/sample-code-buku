# Bab 14 - Large Language Model dan Generative AI

Kode pendamping buku *Fundamental Pembelajaran Mesin* (Hendri Karisma), Bab 14.

| Berkas | Isi | Kode di buku |
|---|---|---|
| `bpe_dari_nol.py` | Pelatihan BPE dari nol pada korpus kecil bahasa Indonesia dan tokenisasi kata baru | Kode 14.1 |
| `tokenizer_hf.py` | Tokenizer GPT-2 dari Hugging Face; membandingkan jumlah token kalimat Inggris dan Indonesia | Kode 14.2 |
| `generate_decoding.py` | Greedy, temperature, top-p dengan GPT-2; peluang token berikutnya; perplexity | Kode 14.3 |
| `decoding_numpy.py` | Memeriksa contoh hitungan temperature dan top-p | (contoh di Subbab 14.3) |
| `rag_minimal.py` | RAG minimal: embedding E5, pencarian kosinus, recall@k, prompt, panggilan opsional ke server LLM kompatibel OpenAI | Kode 14.4 |
| `bpe-rust/` | Pelatihan dan penerapan aturan merge BPE dalam Rust tanpa crate | (disebut di Subbab 14.2) |

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python bpe_dari_nol.py          # tanpa unduhan
python decoding_numpy.py        # tanpa unduhan
python tokenizer_hf.py          # mengunduh tokenizer GPT-2
python generate_decoding.py     # mengunduh GPT-2 kecil, cukup CPU
python rag_minimal.py           # mengunduh model embedding multilingual-e5-small

# opsional: jalankan LLM lokal lalu arahkan rag_minimal.py ke sana
# vllm serve <nama-model>   (lihat dokumentasi vLLM)
# export LLM_URL=http://localhost:8000/v1/chat/completions LLM_MODEL=<nama-model>

cd bpe-rust && cargo run --release
```

Dokumen pada `rag_minimal.py` sengaja fiktif ("Kampus Contoh"). Ganti dengan dokumen yang memang
boleh Anda olah, dan jangan memasukkan data pribadi ke layanan LLM pihak ketiga tanpa dasar
pemrosesan yang sah.
