"""Kode 14.4 - RAG minimal: embedding, pencarian kosinus, dan penyusunan prompt.

Dokumen di bawah FIKTIF ("Kampus Contoh") untuk latihan. Prompt yang dihasilkan
dapat dikirim ke LLM pilihan Anda, misalnya server vLLM lokal yang kompatibel
OpenAI (lihat fungsi tanya_llm; atur variabel lingkungan LLM_URL dan LLM_MODEL).
"""
import json
import os
import urllib.request

import numpy as np
from sentence_transformers import SentenceTransformer

potongan = [
    "Di Kampus Contoh, skripsi boleh diambil setelah lulus 110 SKS.",
    "Di Kampus Contoh, cuti akademik paling lama dua semester.",
    "Di Kampus Contoh, wisuda diadakan dua kali setahun.",
]
model = SentenceTransformer("intfloat/multilingual-e5-small")
E = model.encode(["passage: " + p for p in potongan], normalize_embeddings=True)


def cari(pertanyaan, k=2):
    q = model.encode(["query: " + pertanyaan], normalize_embeddings=True)[0]
    skor = E @ q                       # cosine similarity
    urut = np.argsort(-skor)[:k]
    return [(int(i), float(skor[i])) for i in urut]


def susun_prompt(pertanyaan, hasil):
    konteks = "\n".join(f"[{i + 1}] {potongan[i]}" for i, _ in hasil)
    return ("Jawab HANYA berdasarkan potongan berikut dan sebutkan nomornya. "
            "Jika tidak ada, katakan tidak tahu.\n" + konteks +
            "\nPertanyaan: " + pertanyaan)


def tanya_llm(prompt):
    url = os.environ.get("LLM_URL")    # mis. http://localhost:8000/v1/chat/completions
    if not url:
        return "(LLM_URL belum diatur; prompt hanya dicetak)"
    data = json.dumps({"model": os.environ.get("LLM_MODEL", "model"), "temperature": 0,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(url, data, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # set uji kecil: pertanyaan -> indeks potongan yang benar (untuk recall@k)
    uji = [("Kapan saya boleh mulai skripsi?", 0),
           ("Berapa lama maksimal cuti kuliah?", 1),
           ("Berapa kali wisuda dalam setahun?", 2)]
    benar = 0
    for q, target in uji:
        hasil = cari(q)
        benar += any(i == target for i, _ in hasil)
        print(q, "->", hasil)
    print(f"recall@2 = {benar / len(uji):.2f}\n")

    prompt = susun_prompt(uji[0][0], cari(uji[0][0]))
    print(prompt, "\n")
    print(tanya_llm(prompt))
