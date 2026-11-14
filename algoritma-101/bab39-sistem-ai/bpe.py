"""Bab 39: Byte Pair Encoding (Sennrich dkk. 2016) sebagai algoritma greedy.

Pelatihan: berulang kali menggabung pasangan simbol bertetangga yang paling sering.
Seri frekuensi dipecah dengan memilih pasangan yang paling kecil secara leksikografis
(aturan buku ini supaya hasil dapat diulang; implementasi lain bisa berbeda).
Jalankan: python3 bpe.py
"""
from collections import Counter

END = "_"  # penanda akhir kata (Sennrich memakai </w>)


def split_word(word):
    return tuple(word) + (END,)


def count_pairs(vocab):
    pairs = Counter()
    for symbols, freq in vocab.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[(a, b)] += freq
    return pairs


def merge_pair(symbols, pair):
    out, i = [], 0
    while i < len(symbols):
        if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def train(word_freq, num_merges):
    vocab = {split_word(w): f for w, f in word_freq.items()}
    merges = []
    for _ in range(num_merges):
        pairs = count_pairs(vocab)
        if not pairs:
            break
        best_freq = max(pairs.values())
        best = min(p for p, f in pairs.items() if f == best_freq)  # pilihan greedy
        merges.append((best, best_freq))
        vocab = {merge_pair(s, best): f for s, f in vocab.items()}
    return merges, vocab


def encode(word, merges):
    """Terapkan merge sesuai urutan dipelajari: merge berperingkat paling awal dulu."""
    rank = {pair: i for i, (pair, _) in enumerate(merges)}
    symbols = split_word(word)
    while True:
        cands = [(rank[p], p) for p in zip(symbols, symbols[1:]) if p in rank]
        if not cands:
            return list(symbols)
        _, best = min(cands)
        symbols = merge_pair(symbols, best)


def min_tokens(word, vocab_tokens):
    """Pembanding DP (Bab 29): segmentasi dengan token paling sedikit."""
    s = word + END
    n = len(s)
    best = [0] + [None] * n
    for i in range(1, n + 1):
        for j in range(i):
            if best[j] is not None and s[j:i] in vocab_tokens:
                if best[i] is None or best[j] + 1 < best[i]:
                    best[i] = best[j] + 1
    return best[n]


CORPUS = {"makan": 6, "makanan": 4, "dimakan": 3, "minum": 5, "minuman": 3, "tanam": 2}

if __name__ == "__main__":
    merges, vocab = train(CORPUS, 10)
    for i, ((a, b), f) in enumerate(merges, 1):
        print(f"merge {i}: {a!r} + {b!r} -> {a + b!r} (frekuensi {f})")
    print("vocab akhir:", {" ".join(k): v for k, v in vocab.items()})
    for w in ["makanan", "minuman", "dimakan", "tanaman", "makanlah"]:
        print(f"encode({w!r}) = {encode(w, merges)}")

    assert [a + b for (a, b), _ in merges[:5]] == ["an", "an_", "ak", "mak", "makan_"]
    assert encode("minuman", merges) == ["minum", "an_"]
    assert encode("makanan", merges) == ["mak", "an", "an_"]  # bukan makan + an_

    # kata yang tidak ada di korpus tetap dapat dipecah (tidak ada <unk>)
    assert "".join(encode("tanaman", merges)) == "tanaman" + END

    # greedy tidak selalu menghasilkan token paling sedikit
    toy = {"aa": 3, "aaa": 2}
    m2, _ = train(toy, 2)
    tokens = set("a" + END) | {a + b for (a, b), _ in m2}
    print("contoh greedy:", [a + b for (a, b), _ in m2], encode("aaa", m2),
          "minimum =", min_tokens("aaa", tokens))
    assert encode("aaa", m2) == ["aa", "a", "_"] and min_tokens("aaa", tokens) == 2
    print("semua uji bpe lolos")
